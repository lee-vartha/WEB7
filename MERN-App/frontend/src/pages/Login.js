// importing modules
import React, {useState} from 'react';
import API from '../api';

function Login({setUser, setActiveTab}) {
    const [form, setForm] = useState({email: '', password: ''});
    const [msg, setMsg] = useState('');

    const handleSubmit = async () => {
        try {
            const res = await API.post('/auth/login', form);
            localStorage.setItem("token", res.data.token);
            API.get("/auth/me").then((res2) => {
              setUser(res2.data);
              setActiveTab(res2.data.role === "donor" ? "donor" : "beneficiary");
            })
        } catch (err) {
            console.error("Login has failed:", err.response?.data || err.message);
            setMsg(err.response?.data?.msg || "Login failed - try again!")
        }
    };

    return (
    <div className="bg-white text-black shadow-lg rounded-xl p-8 w-full max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-center mb-6">Login</h2>
      <input className="w-full border p-2 mb-3 rounded"
        placeholder="Email" onChange={e => setForm({ ...form, email: e.target.value })} />
      <input type="password" className="w-full border p-2 mb-3 rounded"
        placeholder="Password" onChange={e => setForm({ ...form, password: e.target.value })} />
      <button onClick={handleSubmit}
        className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600">
        Login
      </button>
      <p className="text-center text-red-500 mt-3">{msg}</p>
    </div>
  );

 }

 export default Login;