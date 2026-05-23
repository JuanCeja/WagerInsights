import { Toaster } from "@/components/ui/sonner"
import Login from "@/pages/Login"
import { Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from "./components/ProtectedRoute"
import Dashboard from "./pages/Dashboard"
import MyBets from "./pages/MyBets"
import Register from "./pages/Register"

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />

        <Route path='/login' element={<Login />} />

        <Route path='/register' element={<Register />} />

        <Route path='/dashboard' element={<Dashboard />} />

        <Route path='/my-bets'
          element={
            <ProtectedRoute>
              <MyBets />
            </ProtectedRoute>
          } />

      </Routes>
      <Toaster position="top-center"/>
    </>
  )
}

export default App