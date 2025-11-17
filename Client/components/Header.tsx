"use client";
import { useRouter, usePathname } from 'next/navigation';
import { Layout, Button, Typography, Space } from 'antd';
import { HomeOutlined, LogoutOutlined } from '@ant-design/icons';
import { useEffect, useState } from 'react';

const { Header: AntHeader } = Layout;
const { Title } = Typography;

export default function Header() {
  const router = useRouter();
  const pathname = usePathname();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any | null>(null);

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    setIsAuthenticated(!!token);
    if (token) {
      const ld = localStorage.getItem('loginData');
      if (ld) setUser(JSON.parse(ld));
    }
  }, [pathname]);

  const handleHome = () => {
    if (isAuthenticated) {
      router.push('/dashboard');
    } else {
      router.push('/login');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('loginData');
    setIsAuthenticated(false);
    setUser(null);
    router.push('/login');
  };

  // Không hiển thị header ở trang login
  if (pathname === '/login') {
    return null;
  }

  return (
    <AntHeader
      style={{
        background: '#fff',
        padding: '0 24px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
        <Title level={4} style={{ margin: 0, cursor: 'pointer' }} onClick={handleHome}>
          🚗 Drive Coach Reservation
        </Title>
       
      </div>

      {isAuthenticated && (
        <Space>
          {user && (
            <span style={{ color: '#666' }}>
              Xin chào, <strong>{user.name || user.username}</strong>
            </span>
          )}
          <Button type="primary" danger icon={<LogoutOutlined />} onClick={handleLogout}>
            Đăng xuất
          </Button>
        </Space>
      )}
    </AntHeader>
  );
}

