"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, Typography, Button, Table, Tag, Space, message, Select } from 'antd';
import { PlusOutlined, EyeOutlined } from '@ant-design/icons';
import api from '../../lib/api';
import dayjs from 'dayjs';

const { Title } = Typography;

export default function ReservesPage() {
  const router = useRouter();
  const [reserves, setReserves] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [user, setUser] = useState<any | null>(null);

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (!token) {
      router.replace('/login');
      return;
    }
    const ld = localStorage.getItem('loginData');
    if (ld) setUser(JSON.parse(ld));
    loadReserves();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter]);

  const loadReserves = async () => {
    setLoading(true);
    try {
      const params = statusFilter !== 'all' ? { status: statusFilter } : {};
      const res = await api.getReserves(params);
      setReserves(res.data || []);
    } catch (err: any) {
      // Không hiển thị error nếu đã redirect về login (401)
      if (err?.response?.status !== 401) {
        // Nếu lỗi là do list rỗng (có thể API trả về 404 hoặc format khác), ta cứ set empty list
        // Tuy nhiên, nếu API chuẩn trả về [], thì không vào catch.
        // Kiểm tra kỹ hơn response
        console.error("Load reserves error:", err);
        setReserves([]);
        // Chỉ hiện lỗi nếu thực sự là lỗi hệ thống, không phải do không có data
        // Tạm thời suppress lỗi hiển thị nếu muốn "không báo lỗi khi list trống"
        // Nhưng nếu API trả 500 thì vẫn nên báo.
        // Giả sử API trả 200 với empty list thì ok.
        // Nếu API trả 404 khi không có data thì ta catch và ignore.
        if (err?.response?.status !== 404) {
          const errMsg = err?.response?.data?.detail || err.message || 'Không thể tải danh sách đặt hẹn';
          message.error(errMsg);
        }
      }
      // Reset reserves nếu có lỗi
      setReserves([]);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: 'Mentor ID',
      dataIndex: 'mentor_id',
      key: 'mentor_id',
      width: 100,
    },
    {
      title: 'Car ID',
      dataIndex: 'car_id',
      key: 'car_id',
      width: 100,
    },
    {
      title: 'Trạng thái',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      render: (status: string) => {
        const colorMap: Record<string, string> = {
          pending: 'orange',
          confirmed: 'green',
          cancelled: 'red',
          completed: 'blue',
          in_progress: 'processing',
        };
        const textMap: Record<string, string> = {
          pending: 'Chờ xác nhận',
          confirmed: 'Đã xác nhận',
          cancelled: 'Đã hủy',
          completed: 'Hoàn thành',
          in_progress: 'Đang diễn ra',
        };
        return <Tag color={colorMap[status] || 'default'}>{textMap[status] || status}</Tag>;
      },
    },
    {
      title: 'Số buổi học',
      key: 'session_count',
      width: 120,
      render: (_: any, record: any) => record.reserve_details?.length || 0,
    },
    {
      title: 'Tổng giá',
      key: 'total_price',
      width: 150,
      render: (_: any, record: any) => {
        const total = record.reserve_details?.reduce((sum: number, detail: any) => sum + (detail.price || 0), 0) || 0;
        return total > 0 ? `${total.toLocaleString('vi-VN')} VNĐ` : '-';
      },
    },
    {
      title: 'Ngày tạo',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 180,
      render: (date: string) => (date ? dayjs(date).format('DD/MM/YYYY HH:mm') : '-'),
    },
    {
      title: 'Thao tác',
      key: 'action',
      width: 120,
      render: (_: any, record: any) => (
        <Button
          type="link"
          icon={<EyeOutlined />}
          onClick={() => router.push(`/reserve/${record.id}`)}
        >
          Chi tiết
        </Button>
      ),
    },
  ];

  return (
    <div style={{ maxWidth: 1200, margin: '24px auto' }}>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Title level={3}>Danh sách đặt hẹn</Title>
          <Space>
            <Select
              value={statusFilter}
              onChange={setStatusFilter}
              style={{ width: 150 }}
              options={[
                { value: 'all', label: 'Tất cả' },
                { value: 'pending', label: 'Chờ xác nhận' },
                { value: 'confirmed', label: 'Đã xác nhận' },
                { value: 'cancelled', label: 'Đã hủy' },
                { value: 'completed', label: 'Hoàn thành' },
                { value: 'in_progress', label: 'Đang diễn ra' },
              ]}
            />
            {!user?.isMentor && (
              <Button type="primary" icon={<PlusOutlined />} onClick={() => router.push('/reserve/new')}>
                Đặt lịch hẹn mới
              </Button>
            )}
          </Space>
        </div>
        <Table
          columns={columns}
          dataSource={reserves}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>
    </div>
  );
}

