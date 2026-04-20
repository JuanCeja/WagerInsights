import { Route, Routes } from 'react-router-dom'

function Login() {
  return (
    <div className='flex min-h-sreen items-center justify-center'>
      <h1 className='text-3xl font-bold'>Login Page</h1>
    </div>
  )
}

function Dashboard() {
  return (
    <div className='flex min-h-sreen items-center justify-center'>
      <h1 className='text-3xl font-bold'>Dashboard Page</h1>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path='/' element={<Login />} />
      <Route path='/dashboard' element={<Dashboard />} />
    </Routes>
  )
}

export default App