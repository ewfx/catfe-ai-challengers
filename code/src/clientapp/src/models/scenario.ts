export interface Scenario {
  feature: string;
  scenarios: { title: string; steps: string[] }[];
}

export interface ProcessStep {
  testcase: string;
  scenario: string;
  given: string;
  when: string;
  then: string;
}

export interface ProcessRepo {
  process_repo: ProcessStep[];
}