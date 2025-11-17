"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Form, Select, InputNumber, Input, Button, Card, Typography, DatePicker, TimePicker, Space, message, Divider } from 'antd';
import { PlusOutlined, MinusCircleOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import api from '../../../lib/api';

const { Title } = Typography;
const { TextArea } = Input;

export default function NewReservePage() {
  const router = useRouter();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
  const [mentors, setMentors] = useState<any[]>([]);
  const [cars, setCars] = useState<any[]>([]);
  const [user, setUser] = useState<any | null>(null);
  const [selectedMentor, setSelectedMentor] = useState<any | null>(null);
  const [selectedCar, setSelectedCar] = useState<any | null>(null);

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (!token) {
      router.replace('/login');
      return;
    }
    const ld = localStorage.getItem('loginData');
    if (ld) {
      const userData = JSON.parse(ld);
      setUser(userData);
      // Load user_id from API
      loadCurrentUser(userData.username);
    }
    // Load mentors and cars in parallel
    Promise.all([loadMentors(), loadCars()]).finally(() => {
      setLoadingData(false);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Auto-calculate prices when mentor or car changes
  useEffect(() => {
    if (selectedMentor && selectedCar) {
      const reserveDetails = form.getFieldValue('reserve_details') || [];
      reserveDetails.forEach((detail: any, index: number) => {
        if (detail.date && detail.start_time && detail.end_time) {
          const calculatedPrice = calculatePrice(detail.start_time, detail.end_time, detail.date);
          if (calculatedPrice > 0) {
            const currentPrice = form.getFieldValue(['reserve_details', index, 'price']);
            if (!currentPrice || currentPrice === 0) {
              form.setFieldValue(['reserve_details', index, 'price'], Math.round(calculatedPrice));
            }
          }
        }
      });
    }
  }, [selectedMentor, selectedCar]);

  const loadCurrentUser = async (username: string) => {
    try {
      const res = await api.getUsers();
      const users = res.data || [];
      const currentUser = users.find((u: any) => u.username === username);
      if (currentUser) {
        setUser((prev: any) => ({ ...prev, id: currentUser.id, user_id: currentUser.id }));
        form.setFieldsValue({ user_id: currentUser.id });
      } else {
        console.warn('User not found in API response');
      }
    } catch (err: any) {
      // Không hiển thị error nếu đã redirect về login (401)
      if (err?.response?.status !== 401) {
        console.error('Failed to load current user:', err);
        message.warning('Không thể tải thông tin user. Vui lòng thử lại.');
      }
    }
  };

  const loadMentors = async () => {
    try {
      const res = await api.getMentors();
      setMentors(res.data || []);
      return res;
    } catch (err: any) {
      // Không hiển thị error nếu đã redirect về login (401)
      if (err?.response?.status !== 401) {
        const errMsg = err?.response?.data?.detail || err.message || 'Không thể tải danh sách thầy dạy lái xe';
        message.error(errMsg);
      }
      setMentors([]);
      throw err;
    }
  };

  const loadCars = async () => {
    try {
      const res = await api.getCars('available');
      setCars(res.data || []);
      return res;
    } catch (err: any) {
      // Không hiển thị error nếu đã redirect về login (401)
      if (err?.response?.status !== 401) {
        const errMsg = err?.response?.data?.detail || err.message || 'Không thể tải danh sách xe';
        message.error(errMsg);
      }
      setCars([]);
      throw err;
    }
  };

  const calculatePrice = (startTime: any, endTime: any, date: any) => {
    if (!startTime || !endTime || !date) return 0;
    
    const mentorPrice = selectedMentor?.price_per_hour || 0;
    const carPrice = selectedCar?.price_per_hour || 0;
    
    if (mentorPrice === 0 && carPrice === 0) return 0;
    
    // Calculate hours
    const start = dayjs(`${date.format('YYYY-MM-DD')} ${startTime.format('HH:mm')}`);
    const end = dayjs(`${date.format('YYYY-MM-DD')} ${endTime.format('HH:mm')}`);
    const hours = end.diff(start, 'hour', true);
    
    return (mentorPrice + carPrice) * hours;
  };


  const onFinish = async (values: any) => {
    if (!user) {
      message.error('User information not found');
      return;
    }

    setLoading(true);
    try {
      // Convert date and time to ISO 8601 format
      const reserve_details = values.reserve_details.map((detail: any) => {
        const date = detail.date.format('YYYY-MM-DD');
        const startTime = detail.start_time.format('HH:mm');
        const endTime = detail.end_time.format('HH:mm');
        
        const start_datetime = `${date}T${startTime}:00+00:00`;
        const end_datetime = `${date}T${endTime}:00+00:00`;

        return {
          start_time: start_datetime,
          end_time: end_datetime,
          price: detail.price,
          notes: detail.notes || '',
          status: 'pending',
        };
      });

      const userId = user?.id || user?.user_id || values.user_id;
      if (!userId) {
        message.error('Không tìm thấy thông tin user. Vui lòng đăng nhập lại.');
        return;
      }

      const payload = {
        user_id: userId,
        mentor_id: values.mentor_id,
        car_id: values.car_id,
        status: 'pending',
        reserve_details: reserve_details.map((detail: any) => ({
          ...detail,
          price: detail.price || 0, // If price is 0 or empty, server will calculate automatically
        })),
      };

      await api.createReserve(payload);
      message.success('Đặt lịch hẹn thành công!');
      router.push('/reserve');
    } catch (err: any) {
      // Không hiển thị error nếu đã redirect về login (401)
      if (err?.response?.status !== 401) {
        const errMsg = err?.response?.data?.detail || err.message || 'Không thể tạo đặt hẹn. Vui lòng thử lại.';
        message.error(errMsg);
      }
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return (
      <div style={{ maxWidth: 900, margin: '24px auto' }}>
        <Card>
          <div style={{ textAlign: 'center', padding: '40px 0' }}>
            <Typography.Text>Đang tải dữ liệu...</Typography.Text>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 900, margin: '24px auto' }}>
      <Card>
        <Title level={3}>Đặt lịch hẹn mới</Title>
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{
            reserve_details: [{}],
          }}
        >
          <Form.Item name="user_id" hidden>
            <Input />
          </Form.Item>

          <Form.Item
            name="mentor_id"
            label="Chọn thầy dạy lái xe"
            rules={[{ required: true, message: 'Vui lòng chọn thầy dạy lái xe' }]}
          >
            <Select
              placeholder="Chọn thầy dạy lái xe"
              showSearch
              onChange={(value) => {
                const mentor = mentors.find((m) => m.id === value);
                setSelectedMentor(mentor);
              }}
              filterOption={(input, option) =>
                (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
              }
              options={mentors.map((m) => ({
                value: m.id,
                label: `${m.name} - ${m.phone} (${m.experience_years} năm, ${(m.price_per_hour || 0).toLocaleString('vi-VN')} VNĐ/giờ)`,
              }))}
            />
          </Form.Item>

          <Form.Item
            name="car_id"
            label="Chọn xe tập lái"
            rules={[{ required: true, message: 'Vui lòng chọn xe tập lái' }]}
          >
            <Select
              placeholder="Chọn xe tập lái"
              showSearch
              onChange={(value) => {
                const car = cars.find((c) => c.id === value);
                setSelectedCar(car);
              }}
              filterOption={(input, option) =>
                (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
              }
              options={cars.map((c) => ({
                value: c.id,
                label: `${c.brand} ${c.model} - ${c.license_plate} (${c.color}, ${c.year}, ${(c.price_per_hour || 0).toLocaleString('vi-VN')} VNĐ/giờ)`,
              }))}
            />
          </Form.Item>

          <Divider>Thông tin các buổi học</Divider>

          <Form.List name="reserve_details">
            {(fields, { add, remove }) => (
              <>
                {fields.map(({ key, name, ...restField }) => (
                  <Card
                    key={key}
                    size="small"
                    style={{ marginBottom: 16 }}
                    title={`Buổi học ${name + 1}`}
                    extra={
                      fields.length > 1 ? (
                        <Button
                          type="text"
                          danger
                          icon={<MinusCircleOutlined />}
                          onClick={() => remove(name)}
                        >
                          Xóa
                        </Button>
                      ) : null
                    }
                  >
                    <Space direction="vertical" style={{ width: '100%' }} size="middle">
                      <Form.Item
                        {...restField}
                        name={[name, 'date']}
                        label="Ngày học"
                        rules={[{ required: true, message: 'Vui lòng chọn ngày học' }]}
                      >
                        <DatePicker 
                          style={{ width: '100%' }} 
                          format="DD/MM/YYYY"
                          onChange={() => {
                            // Recalculate price when date changes
                            const date = form.getFieldValue(['reserve_details', name, 'date']);
                            const startTime = form.getFieldValue(['reserve_details', name, 'start_time']);
                            const endTime = form.getFieldValue(['reserve_details', name, 'end_time']);
                            if (date && startTime && endTime && selectedMentor && selectedCar) {
                              const calculatedPrice = calculatePrice(startTime, endTime, date);
                              if (calculatedPrice > 0) {
                                const currentPrice = form.getFieldValue(['reserve_details', name, 'price']);
                                if (!currentPrice || currentPrice === 0) {
                                  form.setFieldValue(['reserve_details', name, 'price'], Math.round(calculatedPrice));
                                }
                              }
                            }
                          }}
                        />
                      </Form.Item>

                      <Form.Item
                        {...restField}
                        name={[name, 'start_time']}
                        label="Thời gian bắt đầu"
                        rules={[{ required: true, message: 'Vui lòng chọn thời gian bắt đầu' }]}
                      >
                        <TimePicker 
                          style={{ width: '100%' }} 
                          format="HH:mm"
                          onChange={() => {
                            // Recalculate price when start time changes
                            const date = form.getFieldValue(['reserve_details', name, 'date']);
                            const startTime = form.getFieldValue(['reserve_details', name, 'start_time']);
                            const endTime = form.getFieldValue(['reserve_details', name, 'end_time']);
                            if (date && startTime && endTime && selectedMentor && selectedCar) {
                              const calculatedPrice = calculatePrice(startTime, endTime, date);
                              if (calculatedPrice > 0) {
                                const currentPrice = form.getFieldValue(['reserve_details', name, 'price']);
                                if (!currentPrice || currentPrice === 0) {
                                  form.setFieldValue(['reserve_details', name, 'price'], Math.round(calculatedPrice));
                                }
                              }
                            }
                          }}
                        />
                      </Form.Item>

                      <Form.Item
                        {...restField}
                        name={[name, 'end_time']}
                        label="Thời gian kết thúc"
                        rules={[{ required: true, message: 'Vui lòng chọn thời gian kết thúc' }]}
                      >
                        <TimePicker 
                          style={{ width: '100%' }} 
                          format="HH:mm"
                          onChange={() => {
                            // Recalculate price when end time changes
                            const date = form.getFieldValue(['reserve_details', name, 'date']);
                            const startTime = form.getFieldValue(['reserve_details', name, 'start_time']);
                            const endTime = form.getFieldValue(['reserve_details', name, 'end_time']);
                            if (date && startTime && endTime && selectedMentor && selectedCar) {
                              const calculatedPrice = calculatePrice(startTime, endTime, date);
                              if (calculatedPrice > 0) {
                                const currentPrice = form.getFieldValue(['reserve_details', name, 'price']);
                                if (!currentPrice || currentPrice === 0) {
                                  form.setFieldValue(['reserve_details', name, 'price'], Math.round(calculatedPrice));
                                }
                              }
                            }
                          }}
                        />
                      </Form.Item>

                      <Form.Item
                        {...restField}
                        name={[name, 'price']}
                        label="Giá tiền (VNĐ)"
                        rules={[{ required: false }]}
                        tooltip="Để trống hoặc 0 để hệ thống tự động tính giá dựa trên giá mentor và xe"
                      >
                        <InputNumber
                          style={{ width: '100%' }}
                          min={0}
                          placeholder="Để trống để tự động tính"
                          formatter={(value) => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                          parser={(value) => value!.replace(/\$\s?|(,*)/g, '')}
                          onChange={() => {
                            // Recalculate when time changes
                            const date = form.getFieldValue(['reserve_details', name, 'date']);
                            const startTime = form.getFieldValue(['reserve_details', name, 'start_time']);
                            const endTime = form.getFieldValue(['reserve_details', name, 'end_time']);
                            if (date && startTime && endTime && selectedMentor && selectedCar) {
                              const calculatedPrice = calculatePrice(startTime, endTime, date);
                              if (calculatedPrice > 0) {
                                const currentPrice = form.getFieldValue(['reserve_details', name, 'price']);
                                if (!currentPrice || currentPrice === 0) {
                                  form.setFieldValue(['reserve_details', name, 'price'], Math.round(calculatedPrice));
                                }
                              }
                            }
                          }}
                        />
                      </Form.Item>
                      {(() => {
                        const date = form.getFieldValue(['reserve_details', name, 'date']);
                        const startTime = form.getFieldValue(['reserve_details', name, 'start_time']);
                        const endTime = form.getFieldValue(['reserve_details', name, 'end_time']);
                        if (date && startTime && endTime && selectedMentor && selectedCar) {
                          const calculatedPrice = calculatePrice(startTime, endTime, date);
                          if (calculatedPrice > 0) {
                            return (
                              <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                                💡 Giá gợi ý: {Math.round(calculatedPrice).toLocaleString('vi-VN')} VNĐ
                                ({(selectedMentor.price_per_hour || 0).toLocaleString('vi-VN')} + {(selectedCar.price_per_hour || 0).toLocaleString('vi-VN')} VNĐ/giờ)
                              </Typography.Text>
                            );
                          }
                        }
                        return null;
                      })()}

                      <Form.Item {...restField} name={[name, 'notes']} label="Ghi chú">
                        <TextArea rows={2} placeholder="Ghi chú cho buổi học này (tùy chọn)" />
                      </Form.Item>
                    </Space>
                  </Card>
                ))}
                <Form.Item>
                  <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                    Thêm buổi học
                  </Button>
                </Form.Item>
              </>
            )}
          </Form.List>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={loading}>
                Đặt lịch hẹn
              </Button>
              <Button onClick={() => router.back()}>Hủy</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}

