import type { Metadata } from 'next';
import '@xyflow/react/dist/style.css';
import './globals.css';
export const metadata: Metadata = { title: 'Lại tộc · Gia phả chi Diêm Điền', description: 'Không gian lưu giữ cội nguồn, tra cứu gia phả và kết nối các thế hệ họ Lại chi Diêm Điền.' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="vi"><body>{children}</body></html>; }
