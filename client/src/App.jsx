import { useEffect, useState } from 'react'
import { api } from './api'
import './App.css'

export default function App() {

const [status, setStatus] = useState("loading...");

useEffect(() => {
  api("/health")
  .then((data) => setStatus(data.status))
  .catch((err) => setStatus(`error: ${err.message}`));

}, []);
  return (
    <h1>backend {status}</h1>
  )
}
