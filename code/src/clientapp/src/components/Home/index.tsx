import React, { useState } from "react";
import { Button, MenuItem, Select, FormControl, InputLabel, Container, CircularProgress, Checkbox, FormControlLabel, FormGroup, Typography } from "@mui/material";
import Results from '../Results';
import { ProcessRepo, ProcessStep } from '../../models/scenario';

const options = ["Github", "Splunk", "Jira", "Confluence", "Database"];


const Home: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [scenarios, setScenarios] = useState<ProcessStep[]>([]);
  const [formData, setFormData] = useState({
    dropdown1: "",
    dropdown2: "",
    selectedOptions: [] as string[],
  });

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name as string]: value }));
  };

  // Handle checkbox change
  const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name } = event.target;
    setFormData((prev) => ({
      ...prev,
      selectedOptions: prev.selectedOptions.includes(name)
        ? prev.selectedOptions.filter((item) => item !== name) // Remove if unchecked
        : [...prev.selectedOptions, name], // Add if checked
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setScenarios([]);
    console.log(formData);
    try {
      const response = await fetch("http://localhost:8000/process_repoandgenerate_testcases", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          "text": "https://github.com/ram541619/CustomerOnboardFlow.git",
        }),
      });
      const data: ProcessRepo = await response.json();
      setScenarios(data.process_repo);
      setLoading(false);
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <Container>
      <Container maxWidth="sm" sx={{ mt: 4 }}>
        <form onSubmit={handleSubmit}>
          <FormControl fullWidth>
            <InputLabel>Select AppID</InputLabel>
            <Select name="dropdown1" value={formData.dropdown1} onChange={handleChange} label="Select AppID">
              <MenuItem value="option1">MOS</MenuItem>
              <MenuItem value="option2">CRMMS</MenuItem>
            </Select>
          </FormControl>

          <FormControl fullWidth margin="normal">
            <InputLabel>Select Component</InputLabel>
            <Select name="dropdown2" value={formData.dropdown2} onChange={handleChange} label="Select Component">
              <MenuItem value="optionA">CustomerOnboarding</MenuItem>
              <MenuItem value="optionB">CreditCardSystem</MenuItem>
            </Select>
          </FormControl>

          <Typography variant="h6" gutterBottom>
            Select Tools:
          </Typography>

          <FormControl component="fieldset">
            <FormGroup row={true}>
              {options.map((option) => (
                <FormControlLabel
                  key={option}
                  control={
                    <Checkbox
                      checked={formData.selectedOptions.includes(option)}
                      onChange={handleCheckboxChange}
                      name={option}
                    />
                  }
                  label={option}
                />
              ))}
            </FormGroup>
          </FormControl>

          <Button
            type="submit"
            variant="contained"
            fullWidth sx={{ backgroundColor: "#d71e28", mt: 2, mb: 2 }}
            disabled={loading || !formData.dropdown1 || !formData.dropdown2}
          >
            {loading ? <CircularProgress size={24} sx={{ color: "white" }} /> : "Generate Test Cases"}
          </Button>
        </form>
      </Container>
      {scenarios.length > 0 &&
        <Container>
          <Results scenarios={scenarios} />
        </Container>
      }
    </Container>
  );
};

export default Home;
