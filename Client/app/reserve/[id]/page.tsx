"use client";
import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Card, Typography, Button, Descriptions, Tag, Table, Space, message, Spin } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import api from '../../../lib/api';
import dayjs from 'dayjs';

const { Title } = Typography;

export default function ReserveDetailPage() {
  const router = useRouter();
  const params = useParams();
  const reserveId = params?.id as string;
  const [reserve, setReserve] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (!token) {
      router.replace('/login');
      return;
    }
    if (reserveId) {
      loadReserve();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [reserveId]);

  const loadReserve = async () => {
    setLoading(true);
    try {
      const res = await api.getReserveById(Number(reserveId));
      setReserve(res.data);
    } catch (err: any) {
      // Không hiển thị error nếu đã redirect về login (401)
      if (err?.response?.status !== 401) {
        const errMsg = err?.response?.data?.detail || err.message || 'Không thể tải thông tin đặt hẹn';
        message.error(errMsg);
        // Chỉ redirect nếu không phải 401 (đã được interceptor xử lý)
        if (err?.response?.status !== 401 && err?.response?.status !== 403) {
          router.push('/reserve');
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const getStatusTag = (status: string) => {
    const colorMap: Record<string, string> = {
      pending: 'orange',
      confirmed: 'green',
      cancelled: 'red',
      completed: 'blue',
    };
    const textMap: Record<string, string> = {
      pending: 'Chờ xác nhận',
      confirmed: 'Đã xác nhận',
      cancelled: 'Đã hủy',
      completed: 'Hoàn thành',
    };
    return <Tag color={colorMap[status] || 'default'}>{textMap[status] || status}</Tag>;
  };

  const detailColumns = [
    {
      title: 'Ngày học',
      key: 'date',
      width: 120,
      render: (_: any, record: any) => {
        const date = dayjs(record.start_time);
        return date.format('DD/MM/YYYY');
      },
    },
    {
      title: 'Thời gian',
      key: 'time',
      width: 180,
      render: (_: any, record: any) => {
        const start = dayjs(record.start_time);
        const end = dayjs(record.end_time);
        const hours = end.diff(start, 'hour', true);
        return (
          <div>
            <div>{start.format('HH:mm')} - {end.format('HH:mm')}</div>
            <Typography.Text type="secondary" style={{ fontSize: 12 }}>
              ({hours.toFixed(1)} giờ)
            </Typography.Text>
          </div>
        );
      },
    },
    {
      title: 'Giá tiền',
      dataIndex: 'price',
      key: 'price',
      width: 150,
      render: (price: number, record: any) => {
        const start = dayjs(record.start_time);
        const end = dayjs(record.end_time);
        const hours = end.diff(start, 'hour', true);
        const pricePerHour = hours > 0 ? Math.round(price / hours) : 0;
        return (
          <div>
            <div>{price.toLocaleString('vi-VN')} VNĐ</div>
            {pricePerHour > 0 && (
              <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                ({pricePerHour.toLocaleString('vi-VN')} VNĐ/giờ)
              </Typography.Text>
            )}
          </div>
        );
      },
    },
    {
      title: 'Trạng thái',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      render: (status: string) => getStatusTag(status),
    },
    {
      title: 'Ghi chú',
      dataIndex: 'notes',
      key: 'notes',
      render: (notes: string) => notes || '-',
    },
  ];

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!reserve) {
    return (
      <div style={{ maxWidth: 1200, margin: '24px auto' }}>
        <Card>
          <Title level={4}>Không tìm thấy đặt hẹn</Title>
          <Button onClick={() => router.push('/reserve')}>Quay lại danh sách</Button>
        </Card>
      </div>
    );
  }

  const totalPrice = reserve.reserve_details?.reduce((sum: number, detail: any) => sum + (detail.price || 0), 0) || 0;

  return (
    <div style={{ maxWidth: 1200, margin: '24px auto' }}>
      <Card>
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <div>
            <Button icon={<ArrowLeftOutlined />} onClick={() => router.push('/reserve')} style={{ marginBottom: 16 }}>
              Quay lại
            </Button>
            <Title level={3}>Chi tiết đặt hẹn #{reserve.id}</Title>
          </div>

          <Descriptions title="Thông tin đặt hẹn" bordered column={2}>
            <Descriptions.Item label="ID">{reserve.id}</Descriptions.Item>
            <Descriptions.Item label="Trạng thái">{getStatusTag(reserve.status)}</Descriptions.Item>
            <Descriptions.Item label="User ID">{reserve.user_id}</Descriptions.Item>
            <Descriptions.Item label="Mentor ID">{reserve.mentor_id}</Descriptions.Item>
            <Descriptions.Item label="Car ID">{reserve.car_id}</Descriptions.Item>
            <Descriptions.Item label="Ngày tạo">
              {reserve.createdAt ? dayjs(reserve.createdAt).format('DD/MM/YYYY HH:mm:ss') : '-'}
            </Descriptions.Item>
            <Descriptions.Item label="Ngày cập nhật">
              {reserve.updatedAt ? dayjs(reserve.updatedAt).format('DD/MM/YYYY HH:mm:ss') : '-'}
            </Descriptions.Item>
          </Descriptions>

          <Card title="Chi tiết các buổi học" style={{ marginTop: 16 }}>
            <Table
              columns={detailColumns}
              dataSource={reserve.reserve_details || []}
              rowKey="id"
              pagination={false}
            />
            <div style={{ marginTop: 16, textAlign: 'right' }}>
              <Typography.Text strong style={{ fontSize: 16 }}>
                Tổng tiền: {totalPrice.toLocaleString('vi-VN')} VNĐ
              </Typography.Text>
            </div>
          </Card>
        </Space>
      </Card>
    </div>
  );
}

