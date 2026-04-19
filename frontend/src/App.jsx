import { Button } from "@/components/ui/button"

function App() {
  return (
    <div className="flex min-h-screen items-center justify-center gap-4">
      <Button>Default</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="destructive">Destructive</Button>
    </div>
  )
}

export default App