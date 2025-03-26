import React, { useState } from "react";
import { Tabs, Tab, Box, Typography, Accordion, AccordionSummary, AccordionDetails } from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { ProcessStep } from '../../models/scenario';

interface Props {
  scenarios: ProcessStep[];
}

const Results: React.FC<Props> = ({ scenarios }) => {
  const [tabIndex, setTabIndex] = useState(0);

  return (
    <Box sx={{ width: "100%", p: 2 }}>
      <Tabs value={tabIndex} onChange={(_, newValue) => setTabIndex(newValue)}>
        <Tab label="Scenarios" />
        <Tab label="Test Cases" />
      </Tabs>
      <Box sx={{ mt: 2 }}>
        {tabIndex === 0 && (
          <Box>
            {scenarios.map((step, index) => (
              <Accordion key={index}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="h6">Scenario {index + 1}: {step.Scenario}</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography><strong>Given:</strong> {step.Given}</Typography>
                  <Typography><strong>When:</strong> {step.When}</Typography>
                  <Typography><strong>Then:</strong> {step.Then}</Typography>
                </AccordionDetails>
              </Accordion>
            ))}
          </Box>
        )}
        {tabIndex === 1 && (
          <Typography variant="body1">Test cases will be listed here...</Typography>
        )}
      </Box>
    </Box>
  );
};

Results.defaultProps = {
  scenarios: [],
};

export default Results;
