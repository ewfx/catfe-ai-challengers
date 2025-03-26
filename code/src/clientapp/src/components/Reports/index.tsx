import { Typography, Container } from "@mui/material";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";


const Reports = () => {
    const barData = [
      { name: "Jan", tests_generated: 400 },
      { name: "Feb", tests_generated: 300 },
      { name: "Mar", tests_generated: 500 },
    ];
  
    const pieData = [
      { name: "Components Used", value: 400 },
      { name: "Components InProgress", value: 300 },
      { name: "Components Completed", value: 300 },
    ];
  
    const COLORS = ["#0088FE", "#00C49F", "#FFBB28"];
  
    return (
      <Container>
        <Typography variant="h4" gutterBottom>
          Reports
        </Typography>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
            <ResponsiveContainer width="50%" height={300}>
            <BarChart data={barData}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="tests_generated" fill="#8884d8" />
            </BarChart>
            </ResponsiveContainer>
            <ResponsiveContainer width="50%" height={300}>
            <PieChart>
                <Tooltip />
                <Pie data={pieData} cx="50%" cy="50%" outerRadius={100} fill="#8884d8" dataKey="value">
                {pieData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
                </Pie>
            </PieChart>
            </ResponsiveContainer>
        </div>
      </Container>
    );
  };

export default Reports;
