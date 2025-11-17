"use client";
import { useRouter } from 'next/navigation';
import LoginForm from '../../components/LoginForm';
import { Card, Typography } from 'antd';
import { useEffect } from 'react';

const { Title } = Typography;

export default function LoginPage() {
  const router = useRouter();

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (token) router.replace('/dashboard');
  }, []);

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
      <Card style={{ width: 420 }}>
        <Title level={3} style={{ textAlign: 'center' }}>
          Drive Coach - Login
        </Title>
        <LoginForm onSuccess={() => router.push('/dashboard')} />
      </Card>
    </div>
  );
}
