export interface Scenario {
  feature: string;
  scenarios: { title: string; steps: string[] }[];
}

export interface ProcessStep {
  Scenario: string;
  Given: string;
  When: string;
  Then: string;
}

export interface ProcessRepo {
  process_repo: ProcessStep[];
}