# Table of Contents
- [Supplementary Discussion (Appendix)](#supplementary-discussion-appendix)
  - [A. ISO/IEC-Informed Operationalization of Security and Privacy Principles](#a-isoiec-informed-operationalization-of-security-and-privacy-principles)
  - [B. Details on System vs LLM Level Issues](#b-details-on-system-vs-llm-level-issues)    
  - [C. Post and Comment Analysis](#c-post-and-comment-analysis)
  - [D. LIDE Features](#d-lide-features)
  - [E. Screening Codebook](#e-binary-relevance-screening-codebook-for-manual-validation)
- [References](#references)
- [Installation Instructions](https://github.com/paper-submission-0/IDESecurityPrivacy/blob/main/instructions.md)



# Supplementary Discussion (Appendix) 
## A. ISO/IEC-Informed Operationalization of Security and Privacy Principles

This section describes how established ISO/IEC security and privacy principles informed the operationalization of our coding protocol. The standards were not used as compliance criteria; rather, they served as an interpretive lens to ensure that the categorization of reported incidents followed widely accepted definitions of security and privacy risks. 

Specifically, security-related issues were interpreted using the ISO/IEC 27001 information security model, which defines protection goals in terms of confidentiality, integrity, and availability. Privacy-related issues were interpreted using the ISO/IEC 29100 privacy framework, which emphasizes purpose limitation, collection limitation, transparency, and appropriate handling of personal or sensitive data. ISO/IEC 27002 was used to contextualize access control as a supporting control mechanism that operationalizes confidentiality and integrity in system behavior.

The table below summarizes how these principles were translated into operational definitions during coding, and how they map to the taxonomy categories derived from developer discussions.

### Table 1: Operationalization of ISO/IEC security and privacy principles in the coding protocol

| Standard Principle | ISO/IEC Reference | Operational Interpretation in This Study | Mapped Taxonomy Category | Example Incident |
|-------------------|-----------------|----------------------------------------|------------------------|----------------|
| Confidentiality | ISO/IEC 27001 | Protection against unauthorized disclosure or access to information assets, including source code, credentials, and configuration artifacts accessed by LIDE components or agents. | C1. Unauthorized File Operations, C7. Unauthorized Data Access, C10. Context Integrity Failures | IDE reads API keys from `.env` file or accesses files outside project scope |
| Integrity | ISO/IEC 27001 | Protection against unauthorized or unintended modification of information or system artifacts, including changes generated or executed by autonomous IDE actions. | C1. Unauthorized File Operations, C3. Unsafe Generation of Code, C4. User-Specified Constraint Violations | IDE modifies project files despite analysis-only instruction |
| Availability | ISO/IEC 27001 | Ensuring information and development environments remain usable and operational, including preventing destructive or unstable automated actions. | C1. Unauthorized File Operations, C2. Operational Safety Issues | IDE deletes files or disrupts the build environment during automated execution |
| Access Control (supporting control) | ISO/IEC 27002 | Failure to enforce authorization boundaries or permission constraints when executing LLM-generated commands or invoking external tools. Access control is treated as a mechanism supporting confidentiality and integrity. | C4. User-Specified Constraint Violations, C5. Third-Party Tools Integration Risks, C7. Unauthorized Data Access | Agent executes commands beyond allowed workspace permissions |
| Purpose Legitimacy and Specification | ISO/IEC 29100 | Collection or transmission of personal or proprietary data beyond task requirements or without clear justification during IDE operation. | C9. Unauthorized Transmission & Collection | Source code or telemetry transmitted externally without explicit approval |
| Collection Limitation | ISO/IEC 29100 | Insufficient disclosure regarding data collection, retention, or secondary use of user data, reducing user awareness or control over information processing. | C6. Lack of Transparency, C8. Privacy Leakage Violations | Conversation history stored or reused without clear notification |
| Context Isolation (derived operational principle) | Derived from ISO/IEC 29100 privacy safeguarding considerations | Failure to isolate session or project contexts leads to unintended reuse or exposure of information across interactions. This principle is derived from privacy safeguarding requirements rather than being explicitly defined in ISO standards. | C10. Context Integrity Failures | Data from one project appears in another session |

---

## B. Details on System vs LLM Level Issues

Our qualitative analysis identified six security issues and five privacy issues from Reddit posts. To better understand the origin of the identified risks, we categorized the issues into **system-level** and **LLM-level** concerns. The labeling was performed through iterative team discussions, focusing on where the primary responsibility lies in the IDE–LLM interaction pipeline. The labeling achieved full consensus (100% agreement) among the authors. Table 1 presents the distribution of these issues across IDEs.

Issues were labeled as **system-level** when they originated from IDE operations, permissions, or execution environments. For example, **Unauthorized File Operations (UFO)** capture unsafe file access or modification, while **Operational Safety Issues (OSI)** reflect risks introduced by automated execution or tooling behavior. Some privacy risks, such as **Unauthorized Data Access (UA)**, also fall into this category because they are driven by IDE-side data handling. In contrast, **LLM-level** issues stem from model behavior or prompt interactions. Examples include **Unsafe Generation of Code (UG)**, where models produce insecure outputs, and **Privacy Leakage Violations (PLV)**, where model behavior contributes to unintended disclosure or retention of sensitive information. Certain issues span both layers because model responses and weak system guardrails interact. Table 2 shows that system-level concerns appear more frequently across IDEs.

Across the IDEs presented in Table 2, a clear distinction emerges between system-level and LLM-level issue patterns. IDE-centric environments such as Cursor, Claude-integrated tools, and Codex-based workflows exhibit higher proportions of system-level concerns, particularly **UFO**, **OSI**, and **UA**, suggesting that risks often originate from features, file operations, and permission management rather than purely model behavior. For example, Codex and Replit show strong concentrations of **UFO**, indicating that aggressive execution or modification capabilities at the IDE layer introduce operational risks. Conversely, LLM-level issues such as **UG** and **Privacy Leakage Violations (PLV)** appear more frequently in Copilot and Windsurf, where generation-driven interactions and prompt handling play a larger role. VSCode demonstrates a more balanced distribution, reflecting its modular ecosystem where both extensions and model interactions contribute to risk exposure.

Overall, the system–LLM distinction clarifies responsibility boundaries. LLM-level risks relate to generation safety and prompt robustness. System-level risks relate to integration design and permission handling. The dominance of system-level categories in Table 1 indicates that stronger IDE guardrails could mitigate a large portion of security and privacy issues in LLM-assisted development environments.

### Table 2: Comparative percentage (%) distribution of system-level and LLM-level security and privacy issues across IDEs

<table>
  <thead>
    <tr>
      <th rowspan="3">IDE</th>
      <th colspan="5">Security Issues</th>
      <th colspan="6">Privacy Issues</th>
    </tr>
    <tr>
      <th colspan="4">System-Level</th>
      <th colspan="1">LLM-Level</th>
      <th colspan="4">System-Level</th>
      <th colspan="2">LLM-Level</th>
    </tr>
    <tr>
      <th>UFO</th>
      <th>OSI</th>
      <th>USCV</th>
      <th>TPIR</th>
      <th>UG</th>
      <th>LT</th>
      <th>UA</th>
      <th>PLV</th>
      <th>UTC</th>
      <th>CIL</th>
      <th>PLV</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cursor (130)</td>
      <td>30.0</td>
      <td>22.3</td>
      <td>11.5</td>
      <td>3.1</td>
      <td>10.8</td>
      <td>16.2</td>
      <td>12.3</td>
      <td>6.2</td>
      <td>3.1</td>
      <td>1.9</td>
      <td>6.5</td>
    </tr>
    <tr>
      <td>Claude (89)</td>
      <td>31.5</td>
      <td>16.9</td>
      <td>19.1</td>
      <td>6.7</td>
      <td>13.5</td>
      <td>15.7</td>
      <td>7.9</td>
      <td>7.9</td>
      <td>2.2</td>
      <td>4.6</td>
      <td>7.7</td>
    </tr>
    <tr>
      <td>Windsurf (23)</td>
      <td>30.4</td>
      <td>8.7</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>21.7</td>
      <td>21.7</td>
      <td>17.4</td>
      <td>4.3</td>
      <td>8.7</td>
      <td>4.8</td>
      <td>4.8</td>
    </tr>
    <tr>
      <td>Copilot (31)</td>
      <td>19.4</td>
      <td>12.9</td>
      <td>12.9</td>
      <td>0.0</td>
      <td>6.5</td>
      <td>29.0</td>
      <td>9.7</td>
      <td>6.5</td>
      <td>9.7</td>
      <td>0.0</td>
      <td>9.5</td>
    </tr>
    <tr>
      <td>Codex (41)</td>
      <td>58.5</td>
      <td>4.9</td>
      <td>7.3</td>
      <td>0.0</td>
      <td>9.8</td>
      <td>14.6</td>
      <td>12.2</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>VS Code (16)</td>
      <td>12.5</td>
      <td>31.2</td>
      <td>18.8</td>
      <td>12.5</td>
      <td>6.3</td>
      <td>18.8</td>
      <td>12.5</td>
      <td>6.3</td>
      <td>18.8</td>
      <td>0.0</td>
      <td>6.3</td>
    </tr>
    <tr>
      <td>Replit (16)</td>
      <td>50.0</td>
      <td>18.8</td>
      <td>12.5</td>
      <td>0.0</td>
      <td>12.5</td>
      <td>6.3</td>
      <td>6.3</td>
      <td>6.3</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>6.7</td>
    </tr>
    <tr>
      <td>Other (37)</td>
      <td>24.3</td>
      <td>5.4</td>
      <td>8.1</td>
      <td>0.0</td>
      <td>2.7</td>
      <td>16.2</td>
      <td>2.7</td>
      <td>8.1</td>
      <td>13.5</td>
      <td>0.0</td>
      <td>13.6</td>
    </tr>
  </tbody>
</table>

<p><strong>Abbreviations:</strong> UFO = Unauthorized File Operations; OSI = Operational Safety Issues; USCV = User-Specified Constraint Violations; TPIR = Third-Party Tools Integration Risks; UG = Unsafe Generation of Code; LT = Lack of Transparency; UA = Unauthorized Data Access; PLV = Privacy Leakage Violations; UTC = Unauthorized Transmission & Collection; CIL = Context Integrity Failures</p>

---

## C. Post and Comment Analysis

**Phase 1: Tool Identification and Data Acquisition.**  
The data collection process began with the identification of a comprehensive list of LLM-powered IDEs (LIDEs), curated through a multi-source approach involving industry blog posts and tool documentation. Based on these tools, we targeted 46 subreddits, including both IDE-specific communities (e.g., *r/Cursor*) and general programming forums likely to host LIDE-related security and privacy discussions. To overcome Reddit’s standard pagination limits, we utilized the [ArcticShift API](https://github.com/ArthurHeitmann/arctic_shift), which allowed us to collect **1.5 million posts** and **14 million comments** published between January 1, 2023, and March 31, 2026. After automated security/privacy filtering and manual validation, the final relevant subset contained **446 posts** and **6,280 associated comments**. The comprehensive list of all subreddits and corresponding statistics is provided in Table 3.

![Prompt used to classify Reddit posts](figures/prompt_example_post_full.pdf) 
![Prompt used to classify Reddit posts](figures/full.png)  
*Figure 1: Prompt used to classify Reddit posts discussing security and privacy risks in LLM-enabled IDEs.*

---

**Phase 2: Automated Filtering and Prompt Engineering.**  
To isolate security and privacy concerns from this extensive raw dataset, we implemented an automated filtering pipeline using the `gptoss:20b` model via the Ollama framework, hosted on a 160GB GPU server. To ensure the classifier adhered to rigorous industry standards, we grounded our prompt definitions in IEEE and ISO/IEC standards. Specifically:

- **Security issues** were classified based on threats to the Confidentiality, Integrity, and Availability (CIA) triad as defined in ISO/IEC 27001 and 27002, encompassing unauthorized code access, prompt injection exploits, and violations of secure coding practices.  
- **Privacy concerns** were labeled in accordance with ISO/IEC 29100, focusing on instances where LIDE systems exposed or transmitted personally identifiable information (PII) or sensitive code without explicit justification.  

The classification prompt (see Figure 1) underwent several iterations to pass a gold-standard test set, utilizing a strict binary output to minimize hallucination and ensure adherence to these formal definitions.

---

### Table 3: List of collected subreddits and associated statistics

| Subreddit | Total Posts | Total Comments | Filtered Post Count | Filtered Post Comments |
|-----------|------------:|---------------:|--------------------:|-----------------------:|
| AIPromptProgramming | 14,873 | 22,321 | 0 | 0 |
| AI_Agents | 20,401 | 95,122 | 6 | 41 |
| Anthropic | 8,997 | 68,533 | 2 | 9 |
| Artificial | 61,127 | 311,957 | 0 | 0 |
| ArtificialInteligence | 116,159 | 779,280 | 0 | 0 |
| CLine | 1,945 | 10,832 | 7 | 42 |
| ChatGPT | 491,881 | 5,863,312 | 40 | 412 |
| ChatGPTCoding | 18,806 | 138,951 | 22 | 314 |
| ChatGPTPro | 25,153 | 204,366 | 0 | 0 |
| ClaudeAI | 82,214 | 734,079 | 81 | 1,627 |
| GithubCopilot | 7,348 | 57,628 | 22 | 217 |
| IntelliJIDEA | 2,295 | 7,286 | 1 | 0 |
| JetBrains | 4,505 | 28,545 | 5 | 24 |
| LLMDevs | 15,218 | 44,681 | 3 | 14 |
| LanguageTechnology | 5,033 | 12,031 | 0 | 0 |
| LocalLLaMA | 106,231 | 1,361,751 | 3 | 196 |
| MachineLearning | 90,718 | 280,991 | 0 | 0 |
| OpenAI | 100,694 | 1,030,958 | 8 | 71 |
| Python | 46,658 | 232,502 | 0 | 0 |
| RooCode | 2,904 | 20,240 | 2 | 13 |
| TraeIDE | 260 | 535 | 3 | 33 |
| VisualStudioCode | 973 | 924 | 0 | 0 |
| WebStorm | 246 | 637 | 0 | 0 |
| ZedEditor | 2,753 | 11,916 | 7 | 43 |
| aider | 9 | 1 | 0 | 0 |
| boltnew | 119 | 75 | 0 | 0 |
| boltnewbuilders | 4,170 | 13,861 | 1 | 13 |
| codeium | 2,065 | 11,553 | 9 | 81 |
| codex | 6,238 | 52,347 | 22 | 300 |
| copilotx | 2 | 1 | 0 | 0 |
| cpp | 16,278 | 223,684 | 0 | 0 |
| cursor | 24,718 | 180,278 | 110 | 1,206 |
| kilocode | 1,226 | 5,465 | 1 | 8 |
| kiroIDE | 1,229 | 5,805 | 2 | 36 |
| learnmachinelearning | 52,441 | 201,226 | 0 | 0 |
| nocode | 18,808 | 61,549 | 1 | 21 |
| ollama | 9,087 | 52,562 | 0 | 0 |
| perplexity_ai | 15,446 | 93,073 | 1 | 9 |
| programming | 84,670 | 798,275 | 5 | 357 |
| pycharm | 1,675 | 4,440 | 0 | 0 |
| replit | 8,324 | 38,877 | 15 | 127 |
| vibecoding | 42,891 | 251,642 | 44 | 782 |
| vscode | 21,720 | 80,330 | 8 | 135 |
| warpdotdev | 446 | 2,375 | 0 | 0 |
| webdev | 51,000 | 385,807 | 2 | 25 |
| windsurf | 3,917 | 22,577 | 13 | 124 |

---

**Phase 3: Manual Evaluation and Validation of the Posts.**  
While the LLM initially flagged 3,801 posts as relevant, we conducted a rigorous manual evaluation phase to verify the accuracy of these labels. Two researchers dedicated approximately 60 man-hours to a blind review of the flagged content, achieving a **Cohen’s kappa = 0.97**, confirming the effectiveness of the grounded prompt. Following this manual verification, the final dataset was refined to **446 posts** that directly and substantively discuss security or privacy vulnerabilities within LLM-assisted development environments.

---

**Phase 4: Automated Extraction and Label Generation from Comments.**  
Building on the validated set of 446 posts, we analyzed all associated comment threads to capture practitioner-driven mitigation strategies. In total, **6,280 comments** were collected and processed. This phase focused on high-recall extraction of actionable suggestions, intentionally prioritizing coverage over precision.

We employed two large language models (GPT-OSS:20B and Qwen3:32B) to extract explicit security- or privacy-related recommendations from comments using the prompt shown in Figure 2. The prompt instructed the model to return only concrete actions, safeguards, or procedural advice, excluding opinions, confirmations, or general discussions. This initial pass produced **2,737 candidate suggestion fragments**.

![Initial Prompt to collect suggestions](figures/comment_prompt_phase1.pdf)  
![Initial Prompt to collect suggestions](figures/1.png)  
*Figure 2: Initial prompt to collect suggestions from comments.*

To reduce redundancy introduced by paraphrasing and stylistic variation, we applied a semantic merging step using the prompt in Figure 3. Through similarity-based consolidation and manual verification, semantically equivalent suggestions were merged, yielding **13 distinct suggestion topics**. This consolidation enabled scalable abstraction while preserving the diversity of practitioner guidance present in the corpus.

![Prompt to semantically merge suggestion topics](figures/prompt_comment_merge.pdf)  
![Prompt to semantically merge suggestion topics](figures/merge.png)  
*Figure 3: Prompt to semantically merge suggestion topics.*

---

**Phase 5: Codebook Construction and Iterative Prompt Refinement.**  
The 13 mitigation categories resulted from Phase 4 form the structured codebook presented in Table 4. Each category was defined with precise operational boundaries to minimize ambiguity during labeling. The codebook was embedded into a labeling prompt (Figure 4), instructing the LLM to:

1. Assign each comment to **one or more** of the 13 categories,  
2. Label as **not a suggestion** if no actionable guidance was present, or  
3. Label as **uncategorized** if the comment contained a valid suggestion that did not fit any existing category.  

We iteratively refined this prompt through trial-and-error corrections informed by observed labeling failures until the classifier achieved at least **95% accuracy** on a random validation set of 40 manually labeled comments.

---

### Table 4: Structured Codebook Used in Prompt for Labeling

| Category | Definition |
|----------|-----------|
| Secure IDE Configuration | Practices related to securely configuring AI-enabled IDEs, including permission management, access controls, secure default settings, security auditing, vulnerability scanning, and adherence to general security and privacy best practices. |
| Sensitive File Protection | Measures to prevent AI tools from accessing, modifying, or leaking sensitive files and information, such as credentials, environment files, configuration files, and private keys. |
| Manual Code Verification | Human review and manual validation of AI-generated code to identify logical errors, security vulnerabilities, spam, or other unintended or unsafe behavior. |
| Use Version Control | Use of version control systems to track AI-assisted changes, enable rollback or recovery, and maintain accountability and traceability of code modifications. |
| Sandboxing | Isolation of AI agents, tools, or execution environments within restricted or controlled sandboxes to limit their impact on the host system or production environment. |
| Memory/Context Isolation | Controls that prevent unintended persistence, reuse, or cross-session sharing of memory, context, or data used by AI models or agents. |
| Refer to Documentation | Consulting official documentation to understand AI tool behavior, configuration options, security implications, and known limitations. |
| Consult Vendors | Seeking clarification, guidance, updates, or security assurances from AI IDE vendors or service providers, including updating tools when early releases contain known issues. |
| Disable Telemetry | Disabling automatic data collection, usage tracking, or transmission of usage data to reduce privacy risks and unintended data leakage. |
| Check Organizational Compliance | Ensuring that the use of AI-enabled IDEs complies with organizational policies, internal guidelines, legal requirements, and industry regulations. |
| Logging and Monitoring | Implementing logging and monitoring mechanisms to observe AI actions, detect anomalous behavior, and support auditing and incident investigation. |
| Use Local LLM | Using locally hosted or self-managed language models instead of cloud-based services to retain greater control over data, execution, and privacy. |
| Tool/Extension Monitoring | Verifying, evaluating, and monitoring AI tools or IDE extensions before use or before integrating them into a codebase or repository. |

![Prompt for Labeling the comments using Codebook](figures/prompt_comment_2.pdf)
![Prompt for Labeling the comments using Codebook](figures/2.png)
*Figure 4: Prompt for labeling the comments using the codebook.*

---

**Phase 6: Full-Dataset Labeling and Error Characterization.**  
Using the refined prompt and finalized codebook, 5,725 comments were labeled. The automated labeling produced the following distribution:

- **1,392 comments** assigned to one of the 13 mitigation categories  
- **18 comments** labeled as *uncategorized*  
- **4,317 comments** marked as *not a suggestion*  
- **8 comments** with parsing errors  

Manual validation identified six additional mitigation themes not captured in the automated labeling: **Data Redaction (3)**, **Upgrading Subscription Plans (2)**, **Disconnecting from the Internet (1)**,  and **Data Recovery (1)**. All labeling errors were manually corrected, resulting in a final dataset reflecting the full breadth of practitioner-driven mitigation strategies.


## D. LIDE Features

The AI-assisted features in the table 5 were identified through an exploratory review of LLM-native IDEs (LIDEs). Our research team examined official documentation, release notes, and publicly described capabilities to determine whether features were explicitly supported by AI or LLM components. We then conducted lightweight hands-on checks to validate that the features could be triggered through AI-driven workflows. The shaded cells indicate observed support rather than exhaustive verification; implementations evolve rapidly, and omissions may exist. The goal of the table is to illustrate feature prevalence across LIDEs rather than to provide a definitive benchmark.

The selected features capture common developer–LLM interaction patterns across the development lifecycle. <em>AI Debugging (DEBUG)</em> refers to LLM-assisted diagnosis of errors, stack traces, or failing tests with suggested fixes [1]. <em>AI Documentation (DOCUMENT)</em> includes automatic generation of comments, docstrings, or commit messages from source artifacts [2,3]. <em>AI Refactoring (REFACT)</em> denotes semantic code transformations guided by natural-language instructions [4]. <em>AI Test Generation (TEST)</em> supports synthesizing unit tests or testing scaffolds from existing code [5]. <em>Code Completion (AUTOCOMPLETE)</em> provides inline, context-aware code suggestions during editing [6]. <em>Codebase-Aware Search (SEARCH)</em> enables natural-language querying and navigation across the project context. More advanced capabilities include <em>External Tool Execution (EXTOOL)</em>, where AI agents invoke commands or orchestrate workflows [7,8], and <em>Multi-Modal Input (MMI)</em>, allowing prompts that include images or UI artifacts [9].

Overall, the matrix shows that DEBUG, AUTOCOMPLETE, and SEARCH are widely supported baseline capabilities, while EXTOOL and MMI appear more selectively adopted, reflecting differences in automation scope and design priorities across LIDEs.


  ### Table 5: LIDE Features
  <table style="border-collapse: collapse; width: 100%;">
    <thead>
      <tr>
        <th style="border: 1px solid black; padding: 4px;">Feature / LIDE</th>
        <!-- Rotated headers -->
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Aider</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Bolt</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Codeium</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Cline</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Cursor</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Copilot</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">JetBrains</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Kilo</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Kiro</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Replit</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Roo</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Trae</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">VS Code</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Warp</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Windsurf</div></th>
        <th style="border: 1px solid black; padding: 4px; width: 30px; text-align:center;"><div style="transform: rotate(-90deg); transform-origin: bottom left;">Zed</div></th>
      </tr>
    </thead>
    <tbody>
      <!-- DEBUG -->
      <tr>
        <td style="border: 1px solid black; padding: 4px;">DEBUG - Code/Bug Debugging</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
      </tr>
      <!-- DOCUMENT -->
      <tr>
        <td style="border: 1px solid black; padding: 4px;">DOCUMENT - Code Documentation</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
      </tr>
      <!-- REFACT -->
      <tr>
        <td style="border: 1px solid black; padding: 4px;">REFACT - Code Refactoring</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
      </tr>
      <!-- TEST -->
      <tr>
        <td style="border: 1px solid black; padding: 4px;">TEST - Test Generation</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;"></td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
      </tr>
      <!-- AUTOCOMPLETE -->
      <tr>
        <td style="border: 1px solid black; padding: 4px;">AUTOCOMPLETE - Code Completion</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
      </tr>
      <!-- SEARCH -->
      <tr>
        <td style="border: 1px solid black; padding: 4px;">SEARCH - Code Search</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
      </tr>
      <!-- EXTOOL -->
      <tr>
        <td style="border: 1px solid black; padding: 4px;">EXTOOL - External Tool Execution</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
        <td style="text-align:center;"></td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
      </tr>
      <!-- MMI -->
      <tr>
        <td style="border: 1px solid black; padding: 4px;">MMI - Multi-Modal Input</td>
        <td style="text-align:center;"></td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
        <td style="text-align:center;"></td>
        <td style="text-align:center;"></td>
        <td style="text-align:center;"></td>
        <td style="text-align:center;"></td>
        <td style="text-align:center;"></td>
        <td style="background-color:#dce6ff;text-align:center;">✅</td>
        <td style="text-align:center;"></td>
        <td style="text-align:center;"></td>
      </tr>
    </tbody>
  </table>
</section>

## E. Binary Relevance-Screening Codebook for Manual Validation

This codebook formalizes the binary inclusion and exclusion criteria used to manually validate posts identified by the LLM filter. It is separate from the taxonomy codebook developed later through open and axial coding.

**Labeling criteria**

Assign a value of 1 if the post can be mapped with any ID from Table 6.

Assign a value of 0 if the post can be mapped with any ID from Table 7.


### Table 6: Codebook for inclusion criteria of relevant security and privacy posts
| ID      | Inclusion signal                                  | Operational interpretation                                                                                                                                                                                                                  | Illustrative examples                                                                                                                                         |
| ------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **I1**  | Unauthorized access or disclosure                 | The tool accesses, reads, reveals, indexes, stores, or otherwise processes information outside the user’s intended or authorized scope.                                                                                                     | Reading `.env` files, credentials, private repositories, proprietary code, personal files, prompts, or project data.                                          |
| **I2**  | Unauthorized or unintended modification           | The tool changes code, files, configurations, permissions, tests, repositories, or system artifacts without appropriate authorization or contrary to user instructions.                                                                     | Editing files despite an analysis-only instruction, overwriting code, changing permissions, or making unrequested commits.                                    |
| **I3**  | Destructive or availability-affecting action      | The tool performs or initiates an action that may delete, corrupt, disable, destabilize, or make development or production resources unavailable.                                                                                           | Deleting project files, dropping a database, breaking a build environment, or disrupting production infrastructure.                                           |
| **I4**  | Permission or control-boundary failure            | The tool bypasses or fails to enforce approval requirements, allowlists, ignore files, workspace boundaries, sandbox restrictions, or other user-defined controls.                                                                          | Ignoring `.cursorignore`, running commands without confirmation, or accessing paths outside the allowed workspace.                                            |
| **I5**  | Unsafe code, command, or dependency               | The tool generates, recommends, modifies, or executes code, commands, tests, or dependencies that introduce a plausible security risk.                                                                                                      | Insecure authentication, missing authorization, exposed secrets, vulnerable code, malicious dependencies, or tests altered to conceal failures.               |
| **I6**  | Unsafe autonomous or tool-mediated behavior       | An LLM-based agent, plugin, connector, MCP server, or external tool performs or enables unsafe actions through the development environment.                                                                                                 | Prompt injection, tool poisoning, malicious hidden instructions, unsafe command execution, or overly broad connector permissions.                             |
| **I7**  | Unauthorized data collection or transmission      | The tool collects, sends, uploads, stores, or exposes user, project, or organizational data without clear authorization or beyond the expected task.                                                                                        | Source code transmitted externally, uncontrolled telemetry, secrets sent to a cloud service, or plaintext storage of conversations.                           |
| **I8**  | Data retention, reuse, or training concern        | The post raises a concrete concern about development data being retained, reused, exposed, or used for model training beyond the expected context.                                                                                          | Proprietary code retained for training, conversations stored for extended periods, or credentials persisting in tool memory.                                  |
| **I9**  | Transparency or administrative-visibility concern | The post identifies unclear, undisclosed, or unexpected practices concerning data handling, retention, telemetry, training, or administrator access.                                                                                        | Unclear privacy policies, unexpected default data collection, or uncertainty about employer access to development activity.                                   |
| **I10** | Context or workspace isolation failure            | Information from one user, project, workspace, session, or conversation appears in or affects another unintended context.                                                                                                                   | Cross-session leakage, cross-project memory contamination, or another user’s content appearing in a conversation.                                             |
| **I11** | Explicit security/privacy warning or assessment   | The post presents a security hardening recommendation, incident report, audit, release note, vulnerability warning, or legal/data-breach concern directly related to an LLM-based developer tool.                                           | Security advisories, permission-related release notes, incident retrospectives, secure-configuration checklists, or warnings about AI-generated applications. |
| **I12** | Other plausible security/privacy issue            | The post describes a concrete security or privacy concern that does not match the examples above but could reasonably affect the confidentiality, integrity, availability, authorization, privacy, or safe operation of development assets. | A previously unseen failure mode involving an LLM-based coding tool.                                                                                          |


### Table 7: Codebook for exclusion criteria of relevant security and privacy posts
| ID     | Exclusion condition                                        | Operational interpretation                                                                                                                                                            | Illustrative examples                                                                                                  |
| ------ | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **E1** | No LLM-based developer-tool context                        | The post does not concern an LLM-based coding assistant, coding agent, AI-enabled IDE, or AI-assisted development workflow.                                                           | Conventional IDE errors, ordinary compiler problems, or general cybersecurity incidents.                               |
| **E2** | General AI discussion without development risk             | The post concerns AI news or usage but contains no coding-tool security or privacy issue.                                                                                             | Model releases, pricing, benchmarks, entertainment, image generation, or general productivity.                         |
| **E3** | Ordinary programming question                              | The post asks for programming help without describing a relevant LLM-tool risk.                                                                                                       | Debugging a function, fixing a syntax error, or configuring a non-AI library.                                          |
| **E4** | Quality problem without security/privacy implications      | The post reports incorrect, buggy, slow, inefficient, or low-quality generated code but identifies no security, privacy, authorization, data-loss, or operational-safety consequence. | Poor formatting, incorrect output, weak code style, or a harmless hallucinated API.                                    |
| **E5** | General cybersecurity unrelated to AI-assisted development | The post discusses cybersecurity but not in connection with an LLM-based developer tool or workflow.                                                                                  | Phishing, malware, network attacks, or web vulnerabilities unrelated to AI coding tools.                               |
| **E6** | App showcase or development discussion without risk        | The post describes building or demonstrating an AI-assisted application but reports no security/privacy issue.                                                                        | Showing a generated website or discussing an AI-built application without mentioning unsafe behavior or data exposure. |
| **E7** | Vague dissatisfaction                                      | The post expresses frustration, distrust, or dislike but does not identify a concrete or reasonably articulated security/privacy concern.                                             | “This tool is terrible” or “I do not trust AI” without further explanation.                                            |



## References 
1. Sourcegraph. 2024. *Debugging Code with Cody.* https://sourcegraph.com/docs/cody/capabilities/debug-code. Accessed 2025.

2. JetBrains. 2024. *AI-Generated Commit Messages.* https://www.jetbrains.com/help/ai-assistant/ai-commit-messages.html. Accessed 2025.

3. JetBrains. 2024. *Generate Documentation with AI Assistant.* https://www.jetbrains.com/help/ai-assistant/generate-documentation-with-ai.html. Accessed 2025.

4. JetBrains. 2024. *Refactoring with AI Assistant.* https://www.jetbrains.com/help/ai-assistant/refactoring-with-ai.html. Accessed 2025.

5. JetBrains. 2024. *Generate Tests with AI Assistant.* https://www.jetbrains.com/help/ai-assistant/generate-tests-with-ai.html. Accessed 2025.

6. GitHub. 2024. *GitHub Copilot Code Completions.* https://docs.github.com/en/copilot/concepts/completions/code-suggestions. Accessed 2025.

7. Cursor. 2024. *Cursor IDE Features.* https://cursor.sh/features. Accessed 2025.

8. GitHub. 2024. *GitHub Copilot Coding Agent.* https://docs.github.com/en/copilot/get-started/features#copilot-coding-agent. Accessed 2025.

9. GitHub. 2024. *Working with Visuals Using AI Models.* https://docs.github.com/en/copilot/reference/ai-models/model-comparison. Accessed 2025.
