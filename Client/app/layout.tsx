import '../styles/globals.css';
import 'antd/dist/reset.css';
import LayoutWrapper from '../components/LayoutWrapper';

export const metadata = {
  title: 'Drive Coach Reservation',
  description: 'Frontend for Drive Coach Reservation',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <LayoutWrapper>{children}</LayoutWrapper>
      </body>
    </html>
  );
}
