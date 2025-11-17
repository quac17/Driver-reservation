"use client";
import { Layout } from 'antd';
import Header from './Header';

const { Content } = Layout;

export default function LayoutWrapper({ children }: { children: React.ReactNode }) {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header />
      <Content style={{ padding: '24px', background: '#f0f2f5' }}>
        {children}
      </Content>
    </Layout>
  );
}

