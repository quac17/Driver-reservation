"use client";
import { useEffect, useState } from 'react';
import { Button, Card, Typography, Row, Col, Space } from 'antd';
import { useRouter } from 'next/navigation';
import { CalendarOutlined, PlusOutlined, UnorderedListOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any | null>(null);

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (!token) {
      router.replace('/login');
      return;
    }
    const ld = localStorage.getItem('loginData');
    if (ld) setUser(JSON.parse(ld));
  }, []);

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      <Card>
        <div style={{ marginBottom: 24 }}>
          <Title level={4}>Dashboard</Title>
          {user ? (
            <div>
              <Text strong>Username:</Text> <Text>{user.username}</Text>
              <br />
              <Text strong>Name:</Text> <Text>{user.name || '-'}</Text>
              <br />
              <Text strong>Is Mentor:</Text> <Text>{user.isMentor ? 'Yes' : 'No'}</Text>
            </div>
          ) : (
            <div>Loading profile...</div>
          )}
        </div>

        <Row gutter={[16, 16]}>
          {!user?.isMentor && (
            <Col xs={24} sm={12} md={8}>
              <Card
                hoverable
                style={{ textAlign: 'center', height: '100%' }}
                onClick={() => router.push('/reserve/new')}
              >
                <PlusOutlined style={{ fontSize: 48, color: '#1890ff', marginBottom: 16 }} />
                <Title level={5}>Đặt lịch hẹn mới</Title>
                <Text type="secondary">Tạo đặt hẹn mới với thầy dạy lái xe</Text>
              </Card>
            </Col>
          )}
          <Col xs={24} sm={12} md={8}>
            <Card
              hoverable
              style={{ textAlign: 'center', height: '100%' }}
              onClick={() => router.push('/reserve')}
            >
              <UnorderedListOutlined style={{ fontSize: 48, color: '#52c41a', marginBottom: 16 }} />
              <Title level={5}>Danh sách đặt hẹn</Title>
              <Text type="secondary">Xem tất cả đặt hẹn của bạn</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Card
              hoverable
              style={{ textAlign: 'center', height: '100%' }}
              onClick={() => router.push('/reserve')}
            >
              <CalendarOutlined style={{ fontSize: 48, color: '#faad14', marginBottom: 16 }} />
              <Title level={5}>Lịch học</Title>
              <Text type="secondary">Xem lịch học của bạn</Text>
            </Card>
          </Col>
        </Row>
      </Card>
    </div>
  );
}
