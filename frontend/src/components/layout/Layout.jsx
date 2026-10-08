import Header from './Header';

export default function Layout({ children, sidebar }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="flex">
        {sidebar}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
