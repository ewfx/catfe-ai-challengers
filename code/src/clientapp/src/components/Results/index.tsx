import React, { useState } from "react";
import { Tabs, Tab, Box, Typography } from "@mui/material";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { materialDark } from "react-syntax-highlighter/dist/esm/styles/prism";

interface Props {
  scenarios: any;
  specflow: string;
}

const Results: React.FC<Props> = ({ scenarios, specflow }) => {
  const [tabIndex, setTabIndex] = useState(0);

  return (
    <Box sx={{ width: "100%", p: 2 }}>
      <Tabs value={tabIndex} onChange={(_, newValue) => setTabIndex(newValue)}>
        <Tab label="Scenarios" />
        <Tab label="BDD Automation Specflow" />
      </Tabs>
      <Box sx={{ mt: 2 }}>
        {tabIndex === 0 && (
          <Box>
            <SyntaxHighlighter language="json" style={materialDark}>
              {JSON.stringify(scenarios ?? {}, null, 2)}
            </SyntaxHighlighter>
          </Box>
        )}
        {tabIndex === 1 && (
          <Box>
            <SyntaxHighlighter language="csharp" style={materialDark}>
              {specflow}
            </SyntaxHighlighter>
          </Box>
        )}
      </Box>
    </Box>
  );
};

Results.defaultProps = {
  scenarios: [],
};

export default Results;
