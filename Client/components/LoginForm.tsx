"use client";
import { Form, Input, Button, message } from 'antd';
import api from '../lib/api';

type Props = {
  onSuccess?: () => void;
};

export default function LoginForm({ onSuccess }: Props) {
  const [form] = Form.useForm();

  const onFinish = async (values: any) => {
    try {
      const { username, password } = values;
      const res = await api.login(username, password);
      if (res && res.data && res.data.access_token) {
        const { access_token, message: msg } = res.data;
        localStorage.setItem('access_token', access_token);
        if (msg && msg.loginData) localStorage.setItem('loginData', JSON.stringify(msg.loginData));
        message.success('Login successful');
        if (onSuccess) onSuccess();
      } else {
        message.error('Unexpected login response');
      }
    } catch (err: any) {
      const errMsg = err?.response?.data?.detail || err.message || 'Login failed';
      message.error(errMsg);
    }
  };

  return (
    <Form form={form} layout="vertical" onFinish={onFinish}>
      <Form.Item name="username" label="Username" rules={[{ required: true, message: 'Please input username' }]}>
        <Input placeholder="username" />
      </Form.Item>

      <Form.Item name="password" label="Password" rules={[{ required: true, message: 'Please input password' }]}>
        <Input.Password placeholder="password" />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" block>
          Login
        </Button>
      </Form.Item>
    </Form>
  );
}
