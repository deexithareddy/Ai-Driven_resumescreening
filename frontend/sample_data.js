// ════════════════════════════════════════════════════════════════════════════
// Sample Data — 55 Industry Domains × 3 Experience Levels
// Structure: { entry: resume, mid: resume, senior: resume, jd: string }
// ════════════════════════════════════════════════════════════════════════════

const SAMPLE_DATA = {

// ─── 1. Software / IT ────────────────────────────────────────────────────
"Software / IT": {
entry: `Aditi Rao — Software Developer (Fresher)
Bangalore, Karnataka | aditi.rao@email.com | +91-98765-43210

SUMMARY
Recent B.Tech graduate in Computer Science with strong fundamentals in data structures, algorithms, and web development. Completed 3 internships and built 5 academic projects including a full-stack e-commerce application.

EDUCATION
B.Tech Computer Science — RV College, Bangalore, 2024 (CGPA: 8.6)

INTERNSHIPS
Web Development Intern — Infosys, Mysore (Jan 2024 – May 2024)
 • Built a leave management dashboard using React and Node.js for internal HR team.
 • Wrote REST APIs in Express.js with MongoDB, handling 200+ employee records.

PROJECTS
 • E-commerce Platform: Full-stack app with React frontend, Django backend, PostgreSQL. Implemented cart, checkout, and Razorpay payment integration.
 • Chat Application: Real-time chat using Socket.io and Node.js. Supports group chats and file sharing.

SKILLS
Python, Java, JavaScript, React, Node.js, Django, HTML/CSS, Git, MySQL, MongoDB, Data Structures, OOP

CERTIFICATIONS
AWS Cloud Practitioner (2024), HackerRank Problem Solving (Gold)`,

mid: `Rahul Menon — Full-Stack Software Engineer
Mumbai, Maharashtra | rahul.menon@email.com | +91-98765-43210

SUMMARY
Software engineer with 4 years of hands-on experience building production-grade web applications using Python and JavaScript. Comfortable across the full stack, from database design to frontend interactivity. Contributed to systems serving 200k+ daily active users at a mid-size fintech company.

EXPERIENCE
Software Engineer — PayRight Technologies, Mumbai (Jan 2021 – Present)
 • Built a real-time payment reconciliation dashboard using Django REST Framework and React, cutting reconciliation time from 8 hours to 45 minutes.
 • Migrated a monolithic Node.js application to microservices on AWS ECS, reducing deployment failures by 60%.
 • Wrote and maintained a PostgreSQL schema handling 12M+ daily transactions with proper indexing and partitioning.
 • Set up CI/CD pipelines via GitHub Actions with automated testing, linting, and staged deployment.

Junior Developer — CodeCraft Solutions, Pune (Jun 2019 – Dec 2020)
 • Developed internal tools in Flask for employee onboarding, leave management, and asset tracking.
 • Integrated Razorpay and Stripe payment gateways for client e-commerce projects.

EDUCATION
B.Tech Computer Science — VIT Vellore, 2019 (CGPA: 8.4)

SKILLS
Python, JavaScript, TypeScript, Django, FastAPI, React, Node.js, PostgreSQL, Redis, Docker, AWS, Git, Linux

CERTIFICATIONS
AWS Certified Developer – Associate (2022)`,

senior: `Srinivas Iyer — Principal Engineer / Tech Lead
Bangalore, Karnataka | srinivas.iyer@email.com | +91-98765-43210

SUMMARY
Principal engineer with 10 years of experience designing and scaling distributed systems. Led engineering teams of 8-15 people across 3 companies. Architected platforms handling 50M+ daily requests. Key contributor to 2 successful startup exits.

EXPERIENCE
Principal Engineer — Razorpay, Bangalore (Apr 2021 – Present)
 • Architecting the payment routing engine processing 50M+ transactions daily across 40+ payment methods.
 • Led the migration from monolith to event-driven microservices using Kafka and gRPC, reducing avg latency from 900ms to 120ms.
 • Managing a team of 12 engineers across 3 squads covering payments, settlements, and fraud detection.
 • Designed the disaster recovery strategy with cross-region failover achieving 99.99% uptime SLA.

Senior Engineer — Flipkart, Bangalore (Jun 2017 – Mar 2021)
 • Built the real-time inventory management system for Big Billion Days sale events handling 10M+ concurrent users.
 • Implemented distributed caching layer with Redis Cluster, reducing database load by 70%.

Software Engineer — TCS, Chennai (Jul 2014 – May 2017)
 • Full-stack development on banking middleware projects using Java Spring Boot and Angular.

EDUCATION
M.Tech Computer Science — IIT Madras, 2014
B.Tech CSE — NIT Trichy, 2012

SKILLS
System design, distributed systems, Java, Python, Go, Kafka, gRPC, Kubernetes, AWS, Terraform, Redis, PostgreSQL, team leadership, architecture review`,

jd: `Software Engineer — FinEdge Solutions, Bangalore

We are looking for a Software Engineer to join our payments infrastructure team. You will work on high-throughput transaction processing systems and customer-facing dashboards.

Requirements:
 • 3+ years of experience in Python or Java backend development
 • Proficiency in at least one frontend framework (React, Angular, or Vue)
 • Experience with relational databases (PostgreSQL or MySQL)
 • Familiarity with REST API design and microservices architecture
 • Experience with cloud platforms (AWS or GCP)
 • Understanding of CI/CD pipelines and containerization (Docker)

Nice to have:
 • Experience with message queues (Kafka, RabbitMQ)
 • Knowledge of TypeScript
 • Exposure to payment gateway integrations`
},

// ─── 2. Data Science / AI / ML ───────────────────────────────────────────
"Data Science / AI / ML": {
entry: `Nisha Patel — Data Science Fresher
Pune, Maharashtra | nisha.patel@email.com | +91-87654-32109

SUMMARY
M.Sc Statistics graduate with hands-on training in Python, machine learning, and data visualization. Completed a 6-month data science bootcamp and built 4 portfolio projects using real-world datasets from Kaggle.

EDUCATION
M.Sc Statistics — Pune University, 2024 (First Class)
B.Sc Mathematics — Fergusson College, 2022

PROJECTS
 • Customer Churn Prediction: Built a classification model using Random Forest and XGBoost on a telecom dataset (10K records). Achieved 84% accuracy with hyperparameter tuning.
 • Sentiment Analysis: Analyzed 50K Amazon product reviews using NLTK and Logistic Regression, built a Streamlit dashboard for visualization.
 • Housing Price Prediction: Linear regression model on Boston Housing data with feature engineering and cross-validation.

INTERNSHIP
Data Analyst Intern — Mu Sigma, Bangalore (Jan 2024 – Jun 2024)
 • Cleaned and transformed 500K+ rows of retail data using Pandas for category analysis.
 • Built Power BI dashboards tracking weekly sales performance for 3 client brands.

SKILLS
Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, SQL, Power BI, Excel, Statistics, Machine Learning basics`,

mid: `Priya Sharma — Data Scientist
Hyderabad, Telangana | priya.sharma@email.com | +91-87654-32109

SUMMARY
Data scientist with 3 years of experience in building ML pipelines, statistical modeling, and deploying models in production. Focused on NLP and recommendation systems. Comfortable working with messy real-world data and communicating findings to non-technical stakeholders.

EXPERIENCE
Data Scientist — Analytica Labs, Hyderabad (Mar 2021 – Present)
 • Built a customer churn prediction model using XGBoost on 2M+ user records, achieving an AUC of 0.87 and helping reduce churn by 15%.
 • Developed a product recommendation engine using collaborative filtering deployed on AWS SageMaker, generating a 12% increase in cross-sell revenue.
 • Created automated data quality checks in Apache Airflow that flagged 300+ anomalies per month across 15 data pipelines.
 • Designed A/B testing frameworks for pricing experiments using Bayesian statistics.

ML Intern — TechVista, Bangalore (Jun 2020 – Feb 2021)
 • Cleaned and preprocessed 500K+ customer support tickets for a text classification project using spaCy and NLTK.
 • Trained a BERT-based intent classifier with 91% accuracy for an internal chatbot.

EDUCATION
M.Tech Data Science — IIIT Hyderabad, 2020
B.Tech ECE — NIT Warangal, 2018

SKILLS
Python, SQL, Pandas, NumPy, Scikit-learn, XGBoost, TensorFlow, PyTorch, spaCy, Spark, Airflow, AWS SageMaker, Tableau, Git`,

senior: `Dr. Arvind Kumar — Lead Data Scientist
Bangalore, Karnataka | arvind.kumar@email.com | +91-87654-32109

SUMMARY
Lead data scientist with 8 years of experience building and deploying machine learning systems at scale. Led a team of 6 data scientists. Published 5 papers in top ML conferences. Expertise in NLP, deep learning, and MLOps.

EXPERIENCE
Lead Data Scientist — Swiggy, Bangalore (Jun 2021 – Present)
 • Leading the ML team responsible for delivery time prediction, demand forecasting, and dynamic pricing models serving 10M+ daily orders.
 • Redesigned the ETA prediction model using transformer architecture, reducing prediction error by 22% over the baseline GBDT model.
 • Built an ML platform on Kubernetes with MLflow and Kubeflow, standardizing model training, versioning, and deployment for 15+ models.
 • Mentoring 6 data scientists and 3 ML engineers on experimentation methodology and production ML best practices.

Senior Data Scientist — Amazon India, Hyderabad (Jan 2018 – May 2021)
 • Built personalization models for product recommendations using deep collaborative filtering on 100M+ user interactions.
 • Designed real-time fraud detection system using LSTM networks, catching 30% more fraudulent transactions.

Data Scientist — Fractal Analytics, Mumbai (Jul 2016 – Dec 2017)
 • Built marketing mix models for FMCG clients using Bayesian regression and time-series analysis.

EDUCATION
Ph.D. Machine Learning — IISc Bangalore, 2016
B.Tech CSE — IIT Bombay, 2012

PUBLICATIONS
5 papers at NeurIPS, ICML, and ACL. h-index: 12`,

jd: `Data Scientist — DataMind Analytics, Bangalore

We need a Data Scientist to work on our predictive analytics platform serving retail and FMCG clients.

Requirements:
 • 2+ years of experience in data science or machine learning roles
 • Strong proficiency in Python (Pandas, Scikit-learn, TensorFlow or PyTorch)
 • Experience building and deploying ML models in production
 • Solid understanding of statistics, hypothesis testing, and A/B testing
 • Experience with SQL and large-scale data processing

Nice to have:
 • Experience with NLP, recommendation systems, or time-series forecasting
 • Familiarity with cloud ML platforms (SageMaker, Vertex AI)`
},

// ─── 3. Cybersecurity ────────────────────────────────────────────────────
"Cybersecurity": {
entry: `Ravi Shankar — Cybersecurity Analyst (Fresher)
Chennai, Tamil Nadu | ravi.shankar@email.com | +91-76543-21098

SUMMARY
B.Tech IT graduate with a focus on network security and ethical hacking. Completed CEH certification and participated in 5 CTF competitions. Built a home lab for practicing penetration testing with Kali Linux.

EDUCATION
B.Tech Information Technology — Anna University, 2024

PROJECTS
 • Network Vulnerability Scanner: Python tool using Nmap library to scan local networks and generate vulnerability reports.
 • Phishing Detection: ML model using Random Forest to classify phishing emails with 89% accuracy on a 10K email dataset.

CERTIFICATIONS
CEH (Certified Ethical Hacker), CompTIA Security+

SKILLS
Networking (TCP/IP, DNS, HTTP), Linux, Kali Linux, Wireshark, Nmap, Burp Suite, Python scripting, OWASP Top 10`,

mid: `Arjun Reddy — Cybersecurity Analyst
Chennai, Tamil Nadu | arjun.reddy@email.com | +91-76543-21098

SUMMARY
Cybersecurity analyst with 4 years of experience in SOC operations, vulnerability assessment, and incident response. Worked in regulated environments (PCI-DSS, ISO 27001) and handled real security incidents affecting production systems.

EXPERIENCE
Senior Security Analyst — SecureNet India, Chennai (Feb 2022 – Present)
 • Monitored and triaged 500+ daily security alerts using Splunk SIEM, reducing false positive rate by 40% through custom correlation rules.
 • Led incident response for a ransomware attack that affected 3 servers, containing the threat within 4 hours.
 • Conducted quarterly penetration tests on web applications using Burp Suite and OWASP ZAP, discovering 25+ critical vulnerabilities.

Security Analyst — CyberGuard Tech, Bangalore (Jul 2019 – Jan 2022)
 • Performed vulnerability scans using Nessus and Qualys across 200+ endpoints.
 • Configured firewall rules on Palo Alto Networks and Cisco ASA devices.

EDUCATION
B.Tech IT — Anna University, 2019

SKILLS
SIEM (Splunk, ELK), Burp Suite, Nessus, Wireshark, Metasploit, Python, Linux, Firewalls, OWASP Top 10

CERTIFICATIONS
CompTIA Security+ (2020), CEH (2021)`,

senior: `Deepika Prasad — CISO / Head of Security
Bangalore, Karnataka | deepika.prasad@email.com | +91-76543-21098

SUMMARY
Chief Information Security Officer with 12 years of experience in enterprise security strategy, compliance, and incident management. Built and led security teams at 3 organizations. Achieved ISO 27001 and SOC 2 Type II certifications.

EXPERIENCE
CISO — Zeta Technologies, Bangalore (Jan 2021 – Present)
 • Leading a 20-person security team covering SOC, AppSec, CloudSec, and Compliance functions for a fintech serving 5M+ users.
 • Designed and implemented the enterprise security architecture including zero-trust network, endpoint detection, and SIEM modernization.
 • Achieved SOC 2 Type II and PCI-DSS Level 1 certifications within 18 months. Passed 3 consecutive audits with zero critical findings.
 • Reduced security incident response time from 6 hours to 45 minutes through automated playbooks and SOAR integration.

Head of Security — InMobi, Bangalore (Mar 2017 – Dec 2020)
 • Built the security function from scratch, hiring and mentoring a team of 12 security engineers.
 • Implemented bug bounty program that identified 200+ vulnerabilities before they reached production.

Security Engineer — Wipro, Hyderabad (Jul 2012 – Feb 2017)

EDUCATION
M.Tech Cybersecurity — IIT Delhi, 2012

CERTIFICATIONS
CISSP, CISM, OSCP, CEH`,

jd: `Cybersecurity Analyst — TrustShield Corp, Hyderabad

We are hiring a Cybersecurity Analyst for our security operations center.

Requirements:
 • 3+ years in cybersecurity, SOC operations, or information security
 • Hands-on experience with SIEM tools (Splunk, QRadar, or ELK)
 • Knowledge of vulnerability assessment tools (Nessus, Qualys, Burp Suite)
 • Experience with incident detection, response, and forensic analysis
 • Understanding of network protocols, firewalls, and IDS/IPS

Nice to have:
 • CEH, OSCP, or CompTIA Security+ certification
 • Cloud security experience (AWS, Azure)`
},

// ─── 4. Cloud Computing / DevOps ─────────────────────────────────────────
"Cloud Computing / DevOps": {
entry: `Ankit Jain — Cloud/DevOps Fresher
Pune, Maharashtra | ankit.jain@email.com | +91-65432-10987

SUMMARY
B.E. graduate with AWS Cloud Practitioner certification. Completed a 3-month DevOps internship working with Docker, Jenkins, and Linux. Built a CI/CD pipeline for a sample Node.js application as a capstone project.

EDUCATION
B.E. Computer Engineering — Pune University, 2024

INTERNSHIP
DevOps Intern — CloudNine Solutions, Pune (Feb 2024 – May 2024)
 • Set up Docker containers for a multi-service application and wrote Docker Compose files.
 • Created a Jenkins pipeline for automated testing and deployment of a Node.js app.
 • Managed EC2 instances and S3 buckets on AWS for a development environment.

PROJECTS
 • Kubernetes Cluster Setup: Deployed a 3-node Kubernetes cluster on AWS using kubeadm, deployed Nginx and a sample Python app with Helm charts.

SKILLS
Linux, Docker, Jenkins, AWS (EC2, S3, IAM), Kubernetes basics, Git, Bash, Python, Terraform basics

CERTIFICATIONS
AWS Cloud Practitioner (2024)`,

mid: `Vikram Singh — DevOps Engineer
Pune, Maharashtra | vikram.singh@email.com | +91-65432-10987

SUMMARY
DevOps engineer with 5 years of experience managing cloud infrastructure, build pipelines, and container orchestration. Primary expertise in AWS and Kubernetes.

EXPERIENCE
Senior DevOps Engineer — CloudScale Technologies, Pune (Apr 2021 – Present)
 • Managed Kubernetes clusters on AWS EKS running 80+ microservices with zero unplanned downtime for 14 months.
 • Wrote Terraform modules for provisioning VPCs, RDS instances, and ECS services, reducing environment setup time from 2 days to 30 minutes.
 • Built CI/CD pipelines in Jenkins and GitLab CI, cutting average build time from 25 minutes to 8 minutes.

DevOps Engineer — InfraWorks, Bangalore (Aug 2018 – Mar 2021)
 • Containerized 15 legacy applications using Docker and deployed them on ECS.
 • Set up Prometheus and Grafana dashboards for monitoring 50+ services.

EDUCATION
B.E. Computer Engineering — Pune University, 2018

SKILLS
AWS (EKS, ECS, Lambda, CloudFormation), Terraform, Kubernetes, Docker, Jenkins, GitLab CI, Ansible, Prometheus, Grafana, ELK Stack, Python, Bash, Linux

CERTIFICATIONS
AWS Solutions Architect – Professional (2022), CKA (2021)`,

senior: `Naveen Reddy — VP of Infrastructure / Platform Engineering Lead
Hyderabad, Telangana | naveen.reddy@email.com | +91-65432-10987

SUMMARY
Infrastructure leader with 11 years of experience building and scaling cloud platforms. Managed teams of 20+ engineers. Architected multi-cloud infrastructure supporting 100M+ monthly active users.

EXPERIENCE
VP of Infrastructure — Freshworks, Chennai (Jun 2020 – Present)
 • Leading a 25-person platform engineering team responsible for AWS and GCP infrastructure supporting 60K+ business customers globally.
 • Architected multi-region active-active deployment achieving 99.995% uptime across all product lines.
 • Reduced cloud spend by 35% ($2M annually) through FinOps practices, spot instances, and right-sizing.
 • Drove the migration from VMs to Kubernetes, transitioning 200+ services to EKS with zero-downtime rolling deployments.

Principal DevOps Engineer — Myntra, Bangalore (Apr 2016 – May 2020)
 • Built the infrastructure platform supporting 10M+ daily users during EORS sale events.

Senior DevOps — Yahoo India, Bangalore (Jul 2013 – Mar 2016)

EDUCATION
M.Tech Cloud Computing — BITS Pilani, 2013

CERTIFICATIONS
AWS Solutions Architect Professional, GCP Professional Cloud Architect, CKA, CKAD`,

jd: `DevOps Engineer — InfraCore Systems, Bangalore

Looking for a DevOps Engineer to build and maintain our cloud infrastructure.

Requirements:
 • 4+ years of DevOps or SRE experience
 • Deep experience with AWS services (EKS, EC2, RDS, S3, IAM)
 • Proficiency in infrastructure-as-code (Terraform or CloudFormation)
 • Container orchestration experience (Kubernetes, Docker)
 • CI/CD pipeline design (Jenkins, GitLab CI, or GitHub Actions)
 • Monitoring and observability (Prometheus, Grafana, ELK)`
},

// ─── 5. Healthcare / Medical ─────────────────────────────────────────────
"Healthcare / Medical": {
entry: `Dr. Meera Joseph — Junior Resident (MBBS)
Trivandrum, Kerala | meera.joseph@email.com | +91-54321-09876

SUMMARY
Fresh MBBS graduate from a government medical college. Completed 1-year internship with rotations in internal medicine, surgery, pediatrics, obstetrics, and emergency department. Passed NEET-PG with a score in the top 15%.

EDUCATION
MBBS — Government Medical College, Trivandrum, 2024 (First Class)

INTERNSHIP ROTATIONS (2023-2024)
 • Internal Medicine (3 months): Managed 15+ patients daily, performed ECG interpretations and blood gas analysis.
 • Emergency Medicine (2 months): Handled trauma cases, cardiac emergencies, and triage protocols.
 • Surgery (3 months): Assisted in 50+ surgeries including appendectomies, hernia repairs, and wound debridement.

SKILLS
Patient examination, clinical diagnosis, ECG interpretation, wound suturing, BLS certified, emergency triage, EMR documentation

REGISTRATIONS
Kerala Medical Council – Provisional Registration`,

mid: `Dr. Ananya Krishnan — General Physician
Kochi, Kerala | dr.ananya@email.com | +91-54321-09876

SUMMARY
General physician with 6 years of clinical experience in outpatient care, emergency medicine, and chronic disease management. Treated 40+ patients daily at a 300-bed multi-specialty hospital.

EXPERIENCE
General Physician — Lakeshore Hospital, Kochi (Jun 2020 – Present)
 • Managing outpatient clinics for general medicine, seeing 40-50 patients daily covering hypertension, diabetes, respiratory infections, and metabolic disorders.
 • Served as COVID-19 ward duty physician during 2020-2021, managing 200+ moderate and severe cases.
 • Conducting weekly health awareness camps in rural areas, screening 100+ patients per camp for diabetes and hypertension.

Junior Resident — Medical College Hospital, Trivandrum (Jul 2017 – May 2020)
 • Rotated through internal medicine, pediatrics, surgery, and emergency departments.
 • Assisted in 150+ minor surgical procedures.

EDUCATION
MBBS — Government Medical College, Trivandrum, 2017 (First Class with Distinction)

SKILLS
Patient examination, clinical diagnosis, ECG interpretation, emergency care, chronic disease management, patient counseling, EMR systems, BLS`,

senior: `Dr. Rajesh Pillai — HOD Internal Medicine / Senior Consultant
Mumbai, Maharashtra | dr.rajesh.pillai@email.com | +91-54321-09876

SUMMARY
Senior consultant in internal medicine with 15 years of experience. Head of Department at a 500-bed tertiary care hospital. Published 20+ papers in peer-reviewed journals. Trained 100+ residents and fellows.

EXPERIENCE
HOD & Senior Consultant — Kokilaben Hospital, Mumbai (Jun 2018 – Present)
 • Leading a department of 8 consultants, 15 residents, and 30 nursing staff providing care for 100+ inpatients daily.
 • Established the hospital's diabetology and metabolic medicine unit, now managing 2000+ diabetic patients annually.
 • Principal investigator for 3 multicenter clinical trials in type 2 diabetes management.
 • Conducting weekly grand rounds and CME sessions for medical staff.

Consultant Physician — Amrita Hospital, Kochi (Jul 2012 – May 2018)

Senior Resident — AIIMS, New Delhi (Jul 2009 – Jun 2012)

EDUCATION
DM Endocrinology — AIIMS, New Delhi, 2012
MD Internal Medicine — CMC Vellore, 2009
MBBS — GMC Trivandrum, 2005

PUBLICATIONS
22 publications, h-index: 9`,

jd: `General Physician — MedLife Clinics, Bangalore

Requirements:
 • MBBS from a recognized university with valid medical council registration
 • 3+ years of clinical experience in outpatient or hospital settings
 • Experience managing common conditions: diabetes, hypertension, respiratory infections
 • Good clinical examination and diagnostic skills
 • Strong communication skills with patients from diverse backgrounds

Preferred:
 • MD in General Medicine (or pursuing)
 • Experience with electronic medical records`
},

// ─── 6. Nursing / Pharmacy ───────────────────────────────────────────────
"Nursing / Pharmacy": {
entry: `Preethi S — Staff Nurse (Fresher)
Chennai, Tamil Nadu | preethi.s@email.com | +91-43210-98765

SUMMARY
B.Sc Nursing graduate with clinical rotations in medical-surgical, pediatric, obstetric, and community health nursing. Completed 6-month internship at a 400-bed hospital.

EDUCATION
B.Sc. Nursing — SRM College of Nursing, Chennai, 2024

CLINICAL ROTATIONS
 • Medical-Surgical Ward: Assisted with 20+ patients daily, performed vital signs monitoring, wound dressing, and medication administration.
 • ICU Rotation (6 weeks): Observed ventilator management, arterial line monitoring, and Code Blue protocols.
 • Community Health: Conducted home visits for 50+ families, health education on hygiene and nutrition.

SKILLS
Patient assessment, vital signs monitoring, IV cannulation, wound dressing, medication administration, BLS certified, EMR documentation

CERTIFICATIONS
BLS (Basic Life Support), Indian Nursing Council – Provisional Registration`,

mid: `Lakshmi Devi — ICU Staff Nurse
Hyderabad, Telangana | lakshmi.devi@email.com | +91-43210-98765

SUMMARY
Registered nurse with 5 years of experience in intensive care units, skilled in ventilator management, hemodynamic monitoring, and post-surgical patient care.

EXPERIENCE
ICU Staff Nurse — Apollo Hospitals, Hyderabad (Aug 2020 – Present)
 • Providing critical care nursing for 4-6 ICU patients per shift including ventilator management, arterial line monitoring, and vasopressor titration.
 • Administered 500+ IV medications and blood transfusions with zero medication errors over 3 years.
 • Trained 8 new nursing staff on ICU protocols, ventilator weaning procedures, and infection control.
 • Active member of the Code Blue response team, participating in 40+ cardiac arrest resuscitations.

Staff Nurse — Care Hospitals, Hyderabad (Jun 2018 – Jul 2020)
 • Worked in the post-surgical ward managing 10-12 patients per shift.

EDUCATION
B.Sc. Nursing — Osmania University, 2018

CERTIFICATIONS
ACLS, BLS, Indian Nursing Council Registration – Active`,

senior: `Mary Thomas — Chief Nursing Officer
Kochi, Kerala | mary.thomas@email.com | +91-43210-98765

SUMMARY
Chief Nursing Officer with 18 years of nursing experience including 8 years in leadership roles. Managed nursing operations for a 600-bed multi-specialty hospital with 400+ nursing staff.

EXPERIENCE
Chief Nursing Officer — Aster Medcity, Kochi (Jan 2019 – Present)
 • Overseeing nursing operations across 25 departments with 420 nurses, 80 nursing aides, and 15 nurse managers.
 • Achieved NABH nursing excellence standards with 98% compliance score in the last 3 consecutive audits.
 • Reduced hospital-acquired infection rate by 40% through implementation of evidence-based nursing protocols.
 • Established a nurse residency program that reduced new nurse turnover from 35% to 12%.

Nursing Superintendent — KIMS Hospital, Trivandrum (Jun 2014 – Dec 2018)
ICU Head Nurse — Medical College Hospital, Trivandrum (Jul 2006 – May 2014)

EDUCATION
M.Sc. Nursing (Critical Care) — RGUHS, 2010
B.Sc. Nursing — Kerala University, 2006

CERTIFICATIONS
ACLS, PALS, Nursing Administration Certificate`,

jd: `ICU Nurse — Fortis Healthcare, Hyderabad

Requirements:
 • B.Sc. Nursing with valid Nursing Council registration
 • 3+ years of ICU or critical care nursing experience
 • Competency in ventilator management and hemodynamic monitoring
 • BLS and ACLS certification
 • Knowledge of infection control protocols`
},

// ─── 7. Biotechnology ────────────────────────────────────────────────────
"Biotechnology": {
entry: `Kavya Menon — Biotech Research Trainee
Bangalore, Karnataka | kavya.menon@email.com

SUMMARY
M.Sc Biotechnology graduate with hands-on lab experience in molecular cloning, PCR, gel electrophoresis, and cell culture techniques from academic projects and a 6-month dissertation.

EDUCATION
M.Sc Biotechnology — Manipal University, 2024
B.Sc Microbiology — Christ University, 2022

DISSERTATION
"Cloning and Expression of Recombinant GFP in E. coli" — Performed molecular cloning using restriction enzymes and ligation, transformed E. coli competent cells, confirmed expression via SDS-PAGE and Western blot.

SKILLS
Molecular cloning, PCR, gel electrophoresis, bacterial cell culture, SDS-PAGE, Western blot, spectrophotometry, aseptic technique, lab safety`,

mid: `Sneha Iyer — Research Scientist (Molecular Biology)
Bangalore, Karnataka | sneha.iyer@email.com

SUMMARY
Research scientist with 4 years of experience in molecular biology and protein engineering. Hands-on expertise in CRISPR gene editing, protein expression and purification. Published 3 peer-reviewed papers.

EXPERIENCE
Research Scientist — BioGenesis Labs, Bangalore (Jan 2021 – Present)
 • Designed and executed CRISPR-Cas9 knockout experiments in mammalian cell lines (HEK293, CHO) with 85% editing efficiency.
 • Developed a high-throughput ELISA screening protocol that reduced screening time from 3 weeks to 5 days.
 • Purified recombinant proteins using FPLC chromatography at multi-milligram scale.

Research Associate — Indian Institute of Science, Bangalore (Jul 2019 – Dec 2020)
 • Cloned and expressed 20+ recombinant protein constructs in E. coli.

EDUCATION
M.Tech Biotechnology — IIT Madras, 2019

SKILLS
CRISPR-Cas9, molecular cloning, protein purification (FPLC), ELISA, Western blot, qPCR, flow cytometry, cell culture`,

senior: `Dr. Suresh Reddy — Director of R&D, Biologics
Hyderabad, Telangana | suresh.reddy@email.com

SUMMARY
R&D director with 14 years of experience in biologics development from discovery to IND filing. Led teams of 25+ scientists. 15 patents and 30+ publications.

EXPERIENCE
Director R&D — Bharat Biotech, Hyderabad (Jun 2018 – Present)
 • Leading a 30-person R&D team developing recombinant protein vaccines and monoclonal antibodies.
 • Directed the analytical characterization and process development for 3 vaccine candidates from lab scale to 2000L manufacturing.
 • Filed 5 IND applications with CDSCO, all approved in first review cycle.

Principal Scientist — Dr. Reddy's Laboratories, Hyderabad (Jan 2013 – May 2018)
Scientist — NCBS, Bangalore (Jul 2010 – Dec 2012)

EDUCATION
Ph.D. Biochemistry — IISc Bangalore, 2010

PUBLICATIONS
32 papers, 15 patents, h-index: 18`,

jd: `Research Scientist — NovaBio Therapeutics, Hyderabad

Requirements:
 • M.Tech/M.Sc/PhD in Biotechnology, Molecular Biology, or Biochemistry
 • 3+ years of wet lab experience in molecular biology techniques
 • Hands-on experience with protein expression, purification, and characterization
 • Knowledge of CRISPR or genome engineering techniques
 • Experience with ELISA, Western blot, and cell-based assays`
},

// ─── 8. Finance / Banking ────────────────────────────────────────────────
"Finance / Banking": {
entry: `Sanjana Gupta — Finance Analyst Trainee
Mumbai, Maharashtra | sanjana.gupta@email.com

SUMMARY
MBA Finance fresher from a reputed B-school with internship experience in equity research. Strong in financial modeling, Excel, and accounting fundamentals.

EDUCATION
MBA Finance — Narsee Monjee (NMIMS), Mumbai, 2024
B.Com (Hons) — St. Xavier's, Kolkata, 2022

INTERNSHIP
Equity Research Intern — Motilal Oswal, Mumbai (Apr 2024 – Jun 2024)
 • Analyzed financial statements and prepared sector notes for 5 mid-cap IT companies.
 • Built a DCF valuation model in Excel for a client presentation.
 • Assisted in preparing quarterly earnings review reports.

SKILLS
Financial modeling, DCF valuation, Excel (VLOOKUP, pivot tables), PowerPoint, equity research, accounting (IFRS basics), Bloomberg basics`,

mid: `Karthik Nair — Financial Analyst
Mumbai, Maharashtra | karthik.nair@email.com

SUMMARY
Financial analyst with 5 years of experience in corporate finance, financial modeling, and equity research. Worked on deal advisory engagements worth INR 500Cr+.

EXPERIENCE
Senior Financial Analyst — ICICI Securities, Mumbai (Mar 2021 – Present)
 • Building DCF, comparable company, and precedent transaction valuation models for M&A advisory mandates.
 • Analyzed financial statements for 15+ equity research reports published quarterly.
 • Presented investment recommendations to C-level executives and board committees.

Financial Analyst — Deloitte India, Mumbai (Jul 2018 – Feb 2021)
 • Performed due diligence on 8 M&A transactions.
 • Built monthly financial reporting dashboards in Power BI for 3 engagement clients.

EDUCATION
MBA Finance — IIM Lucknow, 2018
B.Com (Hons) — SRCC, Delhi University, 2016

SKILLS
Financial modeling (DCF, LBO, comparables), equity research, Excel (advanced VBA), Power BI, Bloomberg Terminal, M&A due diligence

CERTIFICATIONS
CFA Level II Candidate (2023)`,

senior: `Arun Mehta — CFO / VP Finance
Delhi, India | arun.mehta@email.com

SUMMARY
CFO with 16 years of experience in corporate finance, fundraising, and financial strategy for technology companies. Led IPO preparation and 3 successful funding rounds totaling $150M.

EXPERIENCE
CFO — UrbanClap (now Urban Company), Gurgaon (Jan 2019 – Present)
 • Leading finance, accounting, tax, and investor relations functions for a unicorn startup with $300M+ annual revenue.
 • Led Series F fundraising ($255M) including investor roadshows, financial due diligence, and term sheet negotiations.
 • Built financial planning and analysis (FP&A) function from scratch, implementing Anaplan for budgeting and forecasting.

VP Finance — Ola Cabs, Bangalore (Apr 2014 – Dec 2018)
 • Managed financial operations during hyper-growth phase from $20M to $500M annual revenue.

Senior Manager — PwC India, Mumbai (Jul 2008 – Mar 2014)

EDUCATION
CA (ICAI), CFA Charterholder
MBA Finance — ISB Hyderabad, 2008`,

jd: `Financial Analyst — Goldman Sachs, Bangalore

Requirements:
 • MBA Finance or CA/CFA with 3+ years of experience
 • Expertise in financial modeling, valuation (DCF, comps)
 • Strong analytical skills with advanced Excel proficiency
 • Experience in equity research or M&A advisory
 • Knowledge of capital markets`
},

// ─── 9. Accounting ───────────────────────────────────────────────────────
"Accounting": {
entry: `Pooja Agarwal — Articleship Completed CA
Delhi, India | pooja.agarwal@email.com

SUMMARY
Recently qualified Chartered Accountant with 3 years of articleship experience in statutory audit and tax compliance. Completed articleship at a mid-size CA firm handling 15+ clients.

EDUCATION
Chartered Accountant (CA) — ICAI, 2024
B.Com (Hons) — Hansraj College, Delhi University, 2021

ARTICLESHIP
CA Intern — S.K. Mittal & Associates, Delhi (Jul 2021 – Jun 2024)
 • Assisted in statutory audits of 10+ companies across retail, manufacturing, and services sectors.
 • Filed GST returns (GSTR-1, 3B) and TDS returns for 20+ clients.
 • Prepared financial statements and notes for 5 companies under IndAS.
 • Reconciled bank accounts and maintained accounting records in Tally ERP 9.

SKILLS
Statutory audit, GST compliance, income tax, TDS, Tally ERP 9, Excel, IndAS basics, financial statements preparation`,

mid: `Meera Gupta — Senior Audit Associate (CA)
Delhi, India | meera.gupta@email.com

SUMMARY
Chartered accountant with 4 years of experience in statutory audits, tax compliance, and financial reporting. Handled audits for companies with turnover up to INR 200Cr.

EXPERIENCE
Senior Audit Associate — KPMG India, Delhi (Aug 2021 – Present)
 • Conducting statutory audits for 6-8 clients annually across manufacturing, FMCG, and IT sectors.
 • Led audit teams of 3-4 members, planning audit procedures, reviewing workpapers, and drafting audit reports.
 • Identified internal control deficiencies resulting in clients strengthening their financial controls.

Audit Associate — S.R. Batliboi & Associates, Delhi (Jul 2019 – Jul 2021)
 • Assisted in tax audits under Section 44AB and transfer pricing audits.
 • Filed GST, TDS, and income tax returns for 20+ clients.

EDUCATION
Chartered Accountant (CA) — ICAI, 2019
B.Com (Hons) — Hansraj College, Delhi University, 2016

SKILLS
Statutory audit, GST, income tax, TDS, IndAS, Tally ERP 9, SAP FICO, Excel, internal controls`,

senior: `Ravi Krishnamurthy — Partner / Head of Assurance
Mumbai, Maharashtra | ravi.k@email.com

SUMMARY
Senior audit partner with 18 years of experience in assurance, risk advisory, and regulatory compliance. Led audit engagements for 10+ listed companies. Managed a portfolio of clients with combined revenue exceeding INR 10,000Cr.

EXPERIENCE
Partner, Assurance — Deloitte India, Mumbai (Jun 2016 – Present)
 • Leading statutory audit engagements for 8 listed companies in banking, NBFC, and IT sectors with combined revenues exceeding INR 10,000Cr.
 • Managing a team of 40+ professionals across audit, tax, and advisory functions.
 • Served as engagement quality reviewer for 15+ engagements annually.

Director — EY India, Mumbai (Jul 2010 – May 2016)
Senior Manager — PwC India, Mumbai (Jul 2006 – Jun 2010)

EDUCATION
CA (ICAI), CPA (USA), DISA (ICAI)
B.Com — Sydenham College, Mumbai, 2004`,

jd: `Chartered Accountant — Ernst & Young, Mumbai

Requirements:
 • Qualified CA from ICAI with 3+ years of audit experience
 • Knowledge of IndAS and audit procedures
 • Experience with GST, income tax, and TDS
 • Proficiency in Tally, SAP, or other ERP systems`
},

// ─── 10. Insurance ───────────────────────────────────────────────────────
"Insurance": {
entry: `Ananya Desai — Insurance Trainee
Pune, Maharashtra | ananya.desai@email.com

SUMMARY
MBA Insurance Management graduate with internship experience in motor insurance claims processing. Passed IRDAI Licentiate exam.

EDUCATION
MBA Insurance Management — National Insurance Academy, Pune, 2024
B.Com — Fergusson College, Pune, 2022

INTERNSHIP
Claims Processing Intern — New India Assurance, Pune (Mar 2024 – Jun 2024)
 • Processed 200+ motor insurance claims, verifying policy documents, surveyor reports, and settlement calculations.
 • Assisted in customer complaint resolution for 50+ cases.

CERTIFICATIONS
Licentiate — IRDAI

SKILLS
Insurance fundamentals, claims processing, motor/health/fire insurance basics, IRDAI regulations, MS Excel, customer service`,

mid: `Rajesh Kumar — Insurance Underwriter
Hyderabad, Telangana | rajesh.kumar@email.com

SUMMARY
Insurance underwriter with 5 years of experience in risk assessment, policy pricing, and claims evaluation for general insurance products. Processed 1500+ policy applications.

EXPERIENCE
Senior Underwriter — HDFC ERGO, Hyderabad (Mar 2021 – Present)
 • Evaluating risk profiles and pricing commercial insurance policies (fire, marine, liability) with total insured values up to INR 50Cr.
 • Reduced portfolio loss ratio from 68% to 55% over 2 years.
 • Trained a team of 5 junior underwriters.

Underwriter — New India Assurance, Mumbai (Jun 2018 – Feb 2021)
 • Assessed risk and determined premiums for motor, health, and property insurance.
 • Investigated 50+ claims for potential fraud, identifying 8 fraudulent claims worth INR 1.2Cr.

EDUCATION
MBA Insurance Management — National Insurance Academy, Pune, 2018

CERTIFICATIONS
FIII (Fellow of Insurance Institute of India)`,

senior: `Sunil Verma — Chief Underwriting Officer
Mumbai, Maharashtra | sunil.verma@email.com

SUMMARY
Chief Underwriting Officer with 15 years of experience in general insurance. Managed underwriting portfolios worth INR 2,000Cr+ GWP. Led product development for 5 new insurance products.

EXPERIENCE
CUO — ICICI Lombard, Mumbai (Jan 2019 – Present)
 • Leading underwriting strategy for commercial lines with INR 2,500Cr annual GWP across fire, engineering, liability, and marine segments.
 • Developed dynamic pricing models using actuarial analysis and ML, improving underwriting profit by 18%.
 • Restructured reinsurance program achieving 25% cost savings on treaty placements.

VP Underwriting — Bajaj Allianz, Pune (Apr 2013 – Dec 2018)
Manager — Oriental Insurance, Delhi (Jul 2009 – Mar 2013)

EDUCATION
MBA Actuarial Science — NIA, Pune, 2009
ACII (Associate of Chartered Insurance Institute, London)`,

jd: `Underwriter — Bajaj Allianz, Pune

Requirements:
 • 3+ years in general insurance underwriting
 • Knowledge of risk assessment for fire, marine, liability insurance
 • Understanding of IRDAI regulations
 • Experience with policy pricing and documentation`
},

// ─── 11. Marketing / Digital Marketing ───────────────────────────────────
"Marketing / Digital Marketing": {
entry: `Ritika Joshi — Marketing Executive (Fresher)
Mumbai, Maharashtra | ritika.joshi@email.com

SUMMARY
MBA Marketing graduate with internship experience in social media marketing. Managed Instagram and LinkedIn accounts for 3 brands during internship, growing combined follower base by 40%.

EDUCATION
MBA Marketing — Symbiosis Institute, Pune, 2024
B.A. Mass Communication — Christ University, 2022

INTERNSHIP
Social Media Intern — DigiReach Agency, Mumbai (Apr 2024 – Jul 2024)
 • Created and scheduled 80+ social media posts across Instagram, LinkedIn, and Twitter for 3 client brands.
 • Grew one client's Instagram followers from 5K to 8K in 3 months through content strategy and hashtag optimization.
 • Assisted in writing blog posts and email newsletters.

SKILLS
Social media management, content writing, Canva, basic Google Analytics, Instagram/LinkedIn marketing, copywriting, email marketing basics`,

mid: `Neha Saxena — Digital Marketing Manager
Bangalore, Karnataka | neha.saxena@email.com

SUMMARY
Digital marketing manager with 4 years of experience running performance marketing campaigns. Managed annual ad budgets of INR 2Cr+ and consistently delivered ROAS above 4x for B2B SaaS clients.

EXPERIENCE
Digital Marketing Manager — GrowthPulse Agency, Bangalore (May 2021 – Present)
 • Managing paid acquisition campaigns for 5 B2B SaaS clients with a combined monthly spend of INR 18L across Google Ads, LinkedIn Ads, and Meta Ads.
 • Increased lead generation by 140% through landing page optimization and audience segmentation.
 • Set up marketing automation workflows in HubSpot, nurturing 5000+ leads per month.

Marketing Executive — DigiReach Solutions, Mumbai (Jul 2019 – Apr 2021)
 • Created SEO content strategy that grew organic traffic from 15K to 65K monthly sessions.
 • Managed social media accounts for 8 clients.

EDUCATION
MBA Marketing — Symbiosis, Pune, 2019

SKILLS
Google Ads, Meta Ads, LinkedIn Ads, SEO/SEM, HubSpot, Google Analytics, content marketing, email marketing, A/B testing`,

senior: `Siddhartha Roy — CMO / VP Marketing
Bangalore, Karnataka | siddhartha.roy@email.com

SUMMARY
CMO with 13 years of marketing leadership experience across B2B and B2C companies. Built and scaled marketing teams from 5 to 40 people. Drove $50M+ pipeline through integrated marketing strategies.

EXPERIENCE
CMO — Postman, Bangalore (Mar 2020 – Present)
 • Leading a 45-person global marketing team spanning brand, demand gen, product marketing, content, and developer relations.
 • Built the developer community from 3M to 25M+ users through developer-first content strategy and community events.
 • Designed the full-funnel attribution model connecting marketing spend to $100M+ annual pipeline generation.

VP Marketing — Freshworks, Chennai (Jun 2015 – Feb 2020)
 • Scaled marketing from Series B to IPO, building brand awareness in 120+ countries.

Marketing Manager — InMobi, Bangalore (Jul 2011 – May 2015)

EDUCATION
MBA Marketing — IIM Bangalore, 2011
B.Tech — NIT Surathkal, 2009`,

jd: `Digital Marketing Manager — Freshworks, Chennai

Requirements:
 • 3+ years in digital marketing, preferably B2B SaaS
 • Expertise in Google Ads, LinkedIn Ads, and Meta Ads
 • Experience with marketing automation platforms (HubSpot, Marketo)
 • Strong understanding of SEO and content marketing
 • Data-driven approach with proficiency in GA and reporting tools`
},

// ─── 12-50: Remaining Domains (condensed for performance) ────────────────

"Sales / Business Development": {
entry: `Rohit Mishra — Sales Trainee\nAhmedabad | rohit.mishra@email.com\n\nSUMMARY\nBBA graduate with internship experience in B2B sales. Made 500+ cold calls during a 3-month internship at a SaaS company, converting 15 leads.\n\nEDUCATION\nBBA — Gujarat University, 2024\n\nINTERNSHIP\nSales Intern — ZoomInfo India, Ahmedabad (Apr 2024 – Jun 2024)\n • Made 50+ cold calls daily to IT managers and procurement heads.\n • Scheduled 15 product demo meetings for the sales team.\n • Updated CRM records in Salesforce for 200+ prospect accounts.\n\nSKILLS\nCold calling, lead generation, Salesforce basics, MS Office, verbal communication, presentation skills`,
mid: `Amit Patel — Business Development Manager\nAhmedabad | amit.patel@email.com\n\nSUMMARY\nBD manager with 5 years of B2B sales experience for industrial automation products. Consistently exceeded annual targets by 15-25%. Managed 100+ accounts.\n\nEXPERIENCE\nBDM — Siemens India, Ahmedabad (Apr 2021 – Present)\n • Managing Gujarat and Rajasthan territory with annual revenue targets of INR 8Cr.\n • Exceeded sales targets by 22% in FY2023 by developing 12 new key accounts.\n • Conducted 50+ product demonstrations and technical presentations.\n • Negotiated and closed 3 contracts valued above INR 1Cr each.\n\nSales Executive — Schneider Electric, Mumbai (Jun 2018 – Mar 2021)\n • Sold electrical distribution products. Cold-called 20+ prospects daily.\n\nEDUCATION\nMBA Marketing — SP Jain, Mumbai, 2018\nB.E. Electrical — GTU, 2016\n\nSKILLS\nB2B sales, key account management, Salesforce CRM, technical sales, contract negotiation, pipeline management`,
senior: `Sandeep Khanna — VP Sales / Country Head\nMumbai | sandeep.khanna@email.com\n\nSUMMARY\nVP of Sales with 14 years of enterprise sales leadership. Built and managed a 50-person sales organization generating INR 500Cr+ annual revenue. Opened 3 new geographic markets.\n\nEXPERIENCE\nVP Sales India — SAP India, Mumbai (Jun 2019 – Present)\n • Leading India sales team of 55 account executives and pre-sales consultants with INR 600Cr annual revenue target.\n • Grew India business from INR 350Cr to INR 600Cr in 4 years through enterprise account expansion.\n • Closed the largest deal in India history (INR 80Cr TCV) with a top-3 Indian bank.\n\nDirector Sales — Oracle India, Bangalore (Jul 2013 – May 2019)\nSenior Account Manager — IBM India, Delhi (Jul 2010 – Jun 2013)\n\nEDUCATION\nMBA — ISB Hyderabad, 2010\nB.Tech — IIT Roorkee, 2008`,
jd: `Business Development Manager — ABB India, Pune\n\nRequirements:\n • 4+ years B2B sales experience in industrial automation or manufacturing\n • Proven track record of meeting revenue targets\n • Experience with key account management and contract negotiation\n • Proficiency in CRM tools (Salesforce preferred)\n • Engineering background preferred`
},

"Human Resources": {
entry: `Shreya Sharma — HR Trainee\nPune | shreya.sharma@email.com\n\nSUMMARY\nMBA HR fresher with internship experience in recruitment and onboarding. Screened 500+ resumes and coordinated 50+ interviews during a 4-month internship.\n\nEDUCATION\nMBA HR — Symbiosis, Pune, 2024\nB.A. Psychology — Fergusson College, 2022\n\nINTERNSHIP\nHR Intern — TCS, Pune (Feb 2024 – May 2024)\n • Screened 500+ resumes on Naukri and LinkedIn for 10 open positions.\n • Coordinated interview schedules for 50+ candidates across 3 hiring managers.\n • Assisted in new joiner onboarding for 20+ employees including document collection and orientation.\n\nSKILLS\nRecruitment, resume screening, interview coordination, onboarding, MS Office, LinkedIn Recruiter basics, verbal communication`,
mid: `Divya Menon — HR Business Partner\nBangalore | divya.menon@email.com\n\nSUMMARY\nHR professional with 5 years of experience in talent acquisition, employee engagement, and HR operations. Managed hiring for engineering teams at a 500-person tech startup.\n\nEXPERIENCE\nHRBP — UrbanTech Solutions, Bangalore (Jan 2021 – Present)\n • Partnering with 4 engineering managers to hire 60+ engineers annually, maintaining 30-day avg time-to-fill.\n • Designed structured interview framework that improved offer acceptance from 65% to 82%.\n • Rolled out quarterly eNPS surveys and created action plans improving scores from 32 to 58.\n\nHR Executive — TechMatrix, Pune (Aug 2018 – Dec 2020)\n • End-to-end recruitment for 40+ positions per quarter.\n • Administered payroll in Darwinbox for 300+ employees.\n\nEDUCATION\nMBA HR — XLRI Jamshedpur, 2018\n\nSKILLS\nTalent acquisition, HRBP, employee engagement, performance management, Darwinbox, Greenhouse ATS, labor law compliance`,
senior: `Vandana Sethi — CHRO\nMumbai | vandana.sethi@email.com\n\nSUMMARY\nCHRO with 15 years of HR leadership. Built HR functions for 3 companies from 100 to 3000+ employees. Board-level experience in org design, culture transformation, and M&A people integration.\n\nEXPERIENCE\nCHRO — Zomato, Gurgaon (Jan 2020 – Present)\n • Leading all people functions for 5000+ employees across 8 countries.\n • Designed the org restructuring during 2022-23 rightsizing, managing with minimal attrition of key talent.\n • Built the ESOP framework and total rewards strategy for the pre-IPO and post-IPO phases.\n\nVP-HR — Flipkart, Bangalore (Jun 2014 – Dec 2019)\n • Scaled the HR function from 15 to 60+ HR professionals supporting 30,000 employees.\n\nHR Director — HCL Technologies (Jul 2009 – May 2014)\n\nEDUCATION\nMBA HR — TISS Mumbai, 2009\nB.A. Economics — Lady Shri Ram, 2007`,
jd: `HR Business Partner — Swiggy, Bangalore\n\nRequirements:\n • 4+ years HR experience, preferably in tech companies\n • Experience in talent acquisition, engagement, and performance management\n • Knowledge of Indian labor laws\n • Experience with HRMS/ATS tools`
},

"Operations / Supply Chain": {
entry: `Raghav Pillai — Operations Trainee\nChennai | raghav.pillai@email.com\n\nSUMMARY\nMBA Operations fresher with internship in warehouse management at an e-commerce company. Familiar with SAP basics, inventory tracking, and lean concepts.\n\nEDUCATION\nMBA Operations — Great Lakes, Chennai, 2024\n\nINTERNSHIP\nOperations Intern — Amazon India, Chennai (Apr 2024 – Jun 2024)\n • Tracked daily inbound and outbound shipments across 3 fulfillment center zones.\n • Assisted in cycle count audits covering 5000+ SKUs with 98% accuracy.\n • Created Excel dashboards for daily throughput monitoring.\n\nSKILLS\nSupply chain basics, inventory management, SAP basics, Excel (pivot tables, VLOOKUP), lean concepts, warehouse operations`,
mid: `Suresh Rao — Supply Chain Manager\nChennai | suresh.rao@email.com\n\nSUMMARY\nSupply chain professional with 6 years of experience in procurement, inventory optimization, and logistics. Managed vendor relationships worth INR 100Cr+ annually.\n\nEXPERIENCE\nSupply Chain Manager — Samsung India, Chennai (Feb 2021 – Present)\n • Managing end-to-end supply chain for mobile accessories covering procurement, warehousing, and distribution.
 • Negotiated contracts with 25+ vendors, achieving 12% cost reduction.\n • Implemented demand forecasting in SAP IBP, reducing stockouts by 35%.\n\nSupply Chain Executive — ITC Limited, Kolkata (Jul 2017 – Jan 2021)\n • Managed procurement of packaging materials worth INR 40Cr annually.\n\nEDUCATION\nMBA Operations — IIM Tiruchirappalli, 2017\n\nSKILLS\nSupply chain management, procurement, vendor management, SAP MM/IBP, demand forecasting, inventory optimization, lean manufacturing`,
senior: `Manoj Shetty — VP Supply Chain\nMumbai | manoj.shetty@email.com\n\nSUMMARY\nVP Supply Chain with 14 years of experience. Managed end-to-end supply chains for consumer goods companies with INR 5,000Cr+ revenue. Led digital transformation of supply chain operations.\n\nEXPERIENCE\nVP Supply Chain — Hindustan Unilever, Mumbai (Mar 2019 – Present)\n • Leading supply chain operations with 30 manufacturing units, 50+ warehouses, and 7M+ outlets.\n • Reduced end-to-end supply chain cost by 8% through route optimization and warehouse automation.\n • Implemented demand sensing using ML models, improving forecast accuracy from 65% to 82%.\n\nGM Operations — Godrej Consumer, Mumbai (Jun 2013 – Feb 2019)\nManager — P&G India, Hyderabad (Jul 2010 – May 2013)\n\nEDUCATION\nMBA Operations — IIM Ahmedabad, 2010\nB.Tech IE — NIT Calicut, 2008`,
jd: `Supply Chain Manager — Amazon India, Hyderabad\n\nRequirements:\n • 5+ years in supply chain, procurement, or operations\n • Experience with demand planning and inventory optimization\n • Proficiency in SAP or similar ERP\n • Strong analytical skills`
},

"Logistics": {
entry: `Faraz Khan — Logistics Coordinator (Fresher)\nDelhi | faraz.khan@email.com\n\nSUMMARY\nBBA Logistics graduate. 3-month internship in freight coordination. Familiar with shipping documentation and transport management basics.\n\nEDUCATION\nBBA Logistics — Amity University, 2024\n\nINTERNSHIP\nLogistics Intern — DHL India, Gurgaon (Mar 2024 – Jun 2024)\n • Assisted in tracking 100+ daily shipments and updating delivery status in TMS.\n • Helped prepare customs documentation for 30+ international shipments.\n\nSKILLS\nFreight basics, customs documentation, TMS, Excel, GPS tracking, shipping logistics`,
mid: `Mohammad Farooq — Logistics Coordinator\nDelhi | m.farooq@email.com\n\nSUMMARY\nLogistics coordinator with 4 years experience managing freight operations, fleet scheduling, and customs documentation. Handled 500+ shipments monthly.\n\nEXPERIENCE\nLogistics Coordinator — Blue Dart Express, Delhi (May 2021 – Present)\n • Coordinating daily dispatch of 150+ shipments, ensuring 95% on-time delivery.\n • Managing 12 transport vendors, saving INR 15L annually through rate negotiation.\n • Processing customs documentation for 80+ international shipments monthly.\n\nLogistics Executive — DHL, Gurgaon (Jun 2019 – Apr 2021)\n • Managed inbound/outbound logistics for automotive spare parts warehouse.\n\nEDUCATION\nBBA Logistics — Amity University, 2019\n\nSKILLS\nFreight management, customs, TMS, fleet management, route optimization, SAP`,
senior: `Ashok Malhotra — VP Logistics & Distribution\nMumbai | ashok.malhotra@email.com\n\nSUMMARY\nVP Logistics with 16 years managing national distribution networks. Oversaw fleet of 500+ vehicles and warehousing operations across 15 states.\n\nEXPERIENCE\nVP Logistics — Flipkart, Bangalore (Jan 2018 – Present)\n • Leading logistics operations covering 20,000+ pincodes with 100+ fulfillment centers.\n • Reduced average delivery time from 5 days to 2.5 days through network optimization.\n • Managed a fleet of 800+ delivery vehicles and 5000+ last-mile delivery partners.\n\nGM Distribution — Asian Paints, Mumbai (Jul 2010 – Dec 2017)\n\nEDUCATION\nMBA SCM — IIM Indore, 2008`,
jd: `Logistics Manager — FedEx India, Mumbai\n\nRequirements:\n • 3+ years in logistics or freight management\n • Knowledge of customs procedures\n • Experience with TMS systems\n • Fleet operations and route optimization skills`
},

"Manufacturing": {
entry: `Suraj Jadhav — Production Engineer Trainee\nPune | suraj.jadhav@email.com\n\nSUMMARY\nB.E. Mechanical graduate with internship experience in CNC machining and assembly line operations at an automotive component plant.\n\nEDUCATION\nB.E. Mechanical — Pune University, 2024\n\nINTERNSHIP\nProduction Intern — Bajaj Auto, Pune (Jan 2024 – May 2024)\n • Observed CNC machining, assembly, and quality inspection processes on the shop floor.\n • Assisted in maintaining production logs and shift-wise output reports.\n • Learned 5S, Kaizen, and Poka-yoke concepts through shop floor projects.\n\nSKILLS\nManufacturing basics, CNC machining awareness, AutoCAD, SolidWorks, 5S, quality inspection basics, MS Excel`,
mid: `Prakash Bhatt — Production Manager\nPune | prakash.bhatt@email.com\n\nSUMMARY\nProduction manager with 7 years managing 2 CNC production lines. Daily output of 5000+ parts. Led Kaizen projects improving OEE from 72% to 88%.\n\nEXPERIENCE\nProduction Manager — Tata AutoComp, Pune (Apr 2020 – Present)\n • Managing 2 CNC lines manufacturing transmission components with 50+ operators.\n • Reduced scrap rate from 4.5% to 1.8% by implementing SPC and Poka-yoke.\n • Led a Kaizen project improving OEE from 72% to 88% in 6 months.\n\nProduction Engineer — Bharat Forge, Pune (Jun 2016 – Mar 2020)\n\nEDUCATION\nB.E. Mechanical — VJTI Mumbai, 2016\n\nSKILLS\nProduction planning, CNC machining, lean manufacturing, Six Sigma Green Belt, SPC, Kaizen, 5S, SAP PP`,
senior: `Rajendra Kulkarni — VP Manufacturing\nPune | rajendra.k@email.com\n\nSUMMARY\nVP Manufacturing with 18 years leading automotive manufacturing plants. Managed 3 plants with 2000+ employees and INR 1200Cr annual production.\n\nEXPERIENCE\nVP Manufacturing — Mahindra & Mahindra, Nashik (Jan 2018 – Present)\n • Overseeing 3 manufacturing plants producing 200,000+ vehicles annually.\n • Led Industry 4.0 transformation including IoT-based predictive maintenance, reducing unplanned downtime by 40%.\n • Achieved World Class Manufacturing (WCM) Silver certification for Nashik plant.\n\nPlant Head — Tata Motors, Pune (Jun 2012 – Dec 2017)\nProduction Manager — Bajaj Auto, Pune (Jul 2006 – May 2012)\n\nEDUCATION\nM.Tech Production Engineering — IIT Bombay, 2006\nSix Sigma Black Belt`,
jd: `Production Manager — Mahindra, Nashik\n\nRequirements:\n • 5+ years in manufacturing/production management\n • Knowledge of CNC machining or assembly processes\n • Experience with lean manufacturing (Kaizen, 5S, TPM)\n • Six Sigma certification preferred`
},

"Mechanical Engineering": {
entry: `Akash Sharma — Design Engineer Trainee\nBangalore | akash.sharma@email.com\n\nSUMMARY\nB.E. Mechanical graduate with proficiency in SolidWorks and AutoCAD. Built 3 design projects including a drone frame and robotic arm during college.\n\nEDUCATION\nB.E. Mechanical — BMS College, Bangalore, 2024\n\nPROJECTS\n • Quadcopter Frame Design: Designed a lightweight carbon fiber frame in SolidWorks, performed FEA stress analysis.\n • 3-DOF Robotic Arm: Designed and 3D printed a robotic arm with servo motors, programmed using Arduino.\n\nSKILLS\nSolidWorks, AutoCAD, ANSYS basics, GD&T basics, 3D printing, manufacturing processes awareness`,
mid: `Anil Kumar — Mechanical Design Engineer\nBangalore | anil.kumar@email.com\n\nSUMMARY\nDesign engineer with 4 years in product design, FEA simulation, and prototype development for automotive and consumer products.\n\nEXPERIENCE\nDesign Engineer — Bosch India, Bangalore (Jan 2021 – Present)\n • Designing injection-molded housings and sheet metal brackets for automotive sensors using CATIA V5.\n • Conducted FEA analysis using ANSYS, validating designs to OEM durability requirements.\n • Released 15+ component drawings with GD&T per ASME Y14.5 standards.\n\nJunior Engineer — Godrej Appliances, Mumbai (Jul 2019 – Dec 2020)\n\nEDUCATION\nB.E. Mechanical — BMS College, Bangalore, 2019\n\nSKILLS\nCATIA V5, SolidWorks, ANSYS Workbench, AutoCAD, GD&T, injection molding design, sheet metal, DFMEA`,
senior: `Sanjay Kulkarni — Head of Engineering\nPune | sanjay.kulkarni@email.com\n\nSUMMARY\nHead of Engineering with 15 years leading product design teams. Managed 30+ engineers. Delivered 50+ products from concept to production.\n\nEXPERIENCE\nHead of Engineering — Cummins India, Pune (Jan 2018 – Present)\n • Leading a 35-person design team for diesel engine components and systems.\n • Directed the development of a BS-VI compliant diesel engine family, involving 200+ new components.\n • Reduced product development cycle from 18 months to 12 months through concurrent engineering and PLM implementation.\n\nSenior Design Manager — Bosch India, Bangalore (Jun 2012 – Dec 2017)\nDesign Engineer — Tata Motors, Pune (Jul 2009 – May 2012)\n\nEDUCATION\nM.Tech Machine Design — IIT Bombay, 2009`,
jd: `Mechanical Design Engineer — Cummins India, Pune\n\nRequirements:\n • 3+ years in mechanical product design\n • Proficiency in CATIA V5, SolidWorks, or NX\n • Experience with FEA tools (ANSYS or Abaqus)\n • Knowledge of GD&T and manufacturing processes`
},

"Civil Engineering": {
entry: `Snehal Patil — Junior Site Engineer\nPune | snehal.patil@email.com\n\nSUMMARY\nB.E. Civil graduate with 6-month internship experience on a residential construction site. Familiar with RCC construction, AutoCAD drawings, and basic quantity surveying.\n\nEDUCATION\nB.E. Civil — COEP, Pune, 2024\n\nINTERNSHIP\nSite Intern — L&T Construction, Pune (Jan 2024 – Jun 2024)\n • Assisted site engineers in monitoring RCC work, formwork, and reinforcement placement.\n • Prepared bar bending schedules for 10+ structural members.\n • Conducted 20+ concrete cube tests and slump tests.\n\nSKILLS\nAutoCAD, STAAD.Pro basics, RCC construction basics, quantity surveying, concrete testing, MS Excel`,
mid: `Ramesh Patil — Site Engineer\nPune | ramesh.patil@email.com\n\nSUMMARY\nCivil site engineer with 5 years in residential construction. Handled RCC structural work and quantity surveying for projects up to INR 80Cr.\n\nEXPERIENCE\nSite Engineer — L&T Construction, Pune (Aug 2020 – Present)\n • Supervising RCC work for a 22-story residential tower (240 apartments).\n • Managing 80+ laborers, 5 subcontractors, and material deliveries.\n • Preparing monthly RA bills worth INR 2-3Cr with 98% accuracy.\n\nJunior Site Engineer — Shapoorji Pallonji, Mumbai (Jun 2018 – Jul 2020)\n\nEDUCATION\nB.E. Civil — COEP, Pune, 2018\n\nSKILLS\nRCC construction, quantity surveying, AutoCAD, STAAD.Pro, MS Project, quality control, IS codes`,
senior: `Mahesh Deshmukh — VP Projects & Construction\nMumbai | mahesh.deshmukh@email.com\n\nSUMMARY\nVP Projects with 18 years managing large-scale construction projects totaling INR 5000Cr+. Delivered 15 high-rise residential and commercial projects.\n\nEXPERIENCE\nVP Projects — Godrej Properties, Mumbai (Jan 2017 – Present)\n • Overseeing construction of 8 projects across Mumbai and Pune with combined value of INR 3000Cr.\n • Managing 200+ site engineers, 50+ subcontractors, and 5000+ laborers.\n • Achieved IGBC Gold certification for 3 residential projects.\n\nGeneral Manager — L&T Construction, Mumbai (Jul 2010 – Dec 2016)\nProject Manager — Shapoorji Pallonji (Jul 2006 – Jun 2010)\n\nEDUCATION\nM.Tech Structural Engineering — IIT Madras, 2006`,
jd: `Site Engineer — Godrej Properties, Mumbai\n\nRequirements:\n • 3+ years in construction site supervision\n • Knowledge of RCC structural work\n • AutoCAD and MS Project proficiency\n • Understanding of IS codes and RERA compliance`
},

"Electrical Engineering": {
entry: `Prathik R — Electrical Engineer Trainee\nBangalore | prathik.r@email.com\n\nSUMMARY\nB.E. Electrical graduate with skills in AutoCAD Electrical, power systems basics, and electrical panel design fundamentals. 3-month internship at a switchgear manufacturer.\n\nEDUCATION\nB.E. Electrical — R.V. College, Bangalore, 2024\n\nINTERNSHIP\nElectrical Intern — Larsen & Toubro Switchgear, Mysore (Feb 2024 – May 2024)\n • Assisted in testing LT switchgear panels including insulation resistance and functional tests.\n • Created circuit diagrams using AutoCAD Electrical for motor control circuits.\n\nSKILLS\nAutoCAD Electrical, power systems basics, circuit design, ETAP basics, panel design awareness, MS Excel`,
mid: `Sanjay Desai — Electrical Design Engineer\nBangalore | sanjay.desai@email.com\n\nSUMMARY\nElectrical engineer with 5 years in power distribution system design, switchgear specification, and panel engineering.\n\nEXPERIENCE\nElectrical Design Engineer — ABB India, Bangalore (Apr 2021 – Present)\n • Designing LT/HT electrical distribution systems using ETAP for data centers up to 10 MVA.\n • Preparing single-line diagrams, cable sizing calculations, and switchgear specifications.\n • Conducted power system studies including load flow, short circuit, and relay coordination.\n\nElectrical Engineer — Kirloskar Electric, Mysore (Jun 2018 – Mar 2021)\n\nEDUCATION\nB.E. Electrical — R.V. College, Bangalore, 2018\n\nSKILLS\nETAP, AutoCAD Electrical, power distribution, switchgear, cable sizing, relay coordination, panel design`,
senior: `Krishna Murthy — Chief Engineering Officer\nChennai | krishna.murthy@email.com\n\nSUMMARY\nChief Engineering Officer with 16 years managing electrical engineering for power and industrial projects. Led teams of 40+ engineers across multiple geographies.\n\nEXPERIENCE\nCEO — Schneider Electric India, Hyderabad (May 2018 – Present)\n • Leading electrical engineering for utility-scale solar and wind projects totaling 2GW capacity.\n • Managed the design and commissioning of 15+ substations (33kV to 220kV).\n\nHead of Electrical — L&T Power, Chennai (Jul 2012 – Apr 2018)\n\nEDUCATION\nM.Tech Power Systems — IIT Kharagpur, 2008`,
jd: `Electrical Design Engineer — Schneider Electric, Hyderabad\n\nRequirements:\n • 3+ years in electrical system design\n • Proficiency in ETAP or AutoCAD Electrical\n • Knowledge of LT/HT switchgear and power distribution\n • Experience with power system studies`
},

"Electronics": {
entry: `Arun S — Embedded Systems Trainee\nChennai | arun.s@email.com\n\nSUMMARY\nB.E. ECE graduate with academic projects in embedded C programming and Arduino. Built an IoT-based home automation system as final year project.\n\nEDUCATION\nB.E. ECE — SSN College, Chennai, 2024\n\nPROJECTS\n • IoT Home Automation: Built a system using ESP32 and MQTT to control lights and fans via mobile app. Used voltage sensors and relay modules.\n • Line Following Robot: Arduino-based robot with IR sensors, implemented PID control.\n\nSKILLS\nEmbedded C, Arduino, ESP32, basic PCB design (KiCad), I2C/SPI/UART, oscilloscope basics`,
mid: `Kavitha Sundaram — Embedded Systems Engineer\nChennai | kavitha.s@email.com\n\nSUMMARY\nEmbedded engineer with 4 years in firmware development and hardware-software integration for IoT and automotive products.\n\nEXPERIENCE\nEmbedded Engineer — Robert Bosch, Chennai (Mar 2021 – Present)\n • Developing firmware for ARM Cortex-M4 ECU modules for automotive body electronics.\n • Designed CAN bus communication protocols (J1939, UDS) for vehicle diagnostics.\n • Debugged HW-SW integration issues using oscilloscopes and JTAG debuggers.\n\nAssociate Engineer — Texas Instruments, Bangalore (Jul 2019 – Feb 2021)\n\nEDUCATION\nB.E. ECE — SSN College, Chennai, 2019\n\nSKILLS\nEmbedded C, ARM Cortex-M, CAN/LIN, FreeRTOS, I2C/SPI/UART, oscilloscope, JTAG, PCB review`,
senior: `Dr. Venkatesh Rao — Director of Engineering, Semiconductor\nBangalore | venkatesh.rao@email.com\n\nSUMMARY\nDirector of Engineering with 14 years in semiconductor chip design and embedded systems. Led the design of 5 commercial SoC products. Holds 8 patents.\n\nEXPERIENCE\nDirector of Engineering — Qualcomm India, Bangalore (Jan 2018 – Present)\n • Leading a 50-person design team for mobile SoC power management subsystems.\n • Directed the development of 3 commercial PMIC chips used in 100M+ smartphones.\n\nPrincipal Engineer — Intel India, Bangalore (Jul 2013 – Dec 2017)\nDesign Engineer — Broadcom India (Jul 2010 – Jun 2013)\n\nEDUCATION\nPh.D. VLSI Design — IISc Bangalore, 2010\n\nPATENTS\n8 US patents in power management and SoC design`,
jd: `Embedded Systems Engineer — Continental Automotive, Bangalore\n\nRequirements:\n • 3+ years embedded firmware development\n • Proficiency in C/C++ for ARM Cortex\n • Automotive protocols (CAN, LIN)\n • Hardware debugging skills`
},

"Automobile Industry": {
entry: `Vishal Yadav — Automotive Quality Trainee\nGurgaon | vishal.yadav@email.com\n\nSUMMARY\nB.Tech Mechanical fresher with internship experience at an automotive parts manufacturer. Familiar with PPAP documentation and inspection tools (vernier, micrometer, CMM observation).\n\nEDUCATION\nB.Tech Mechanical — DTU, Delhi, 2024\n\nINTERNSHIP\nQuality Intern — Motherson Sumi, Gurgaon (Jan 2024 – May 2024)\n • Assisted in incoming material inspection using vernier calipers and micrometers.\n • Prepared PPAP documentation for 5 new parts.\n • Observed CMM measurements and SPC data collection.\n\nSKILLS\nQuality inspection basics, PPAP awareness, measurement tools, AutoCAD, SolidWorks, MS Excel`,
mid: `Deepak Verma — Automotive Quality Engineer\nGurgaon | deepak.verma@email.com\n\nSUMMARY\nQuality engineer with 5 years in automotive quality. Led IATF 16949 certification. Prepared 50+ PPAP packages with 100% first-time approval.\n\nEXPERIENCE\nSenior Quality Engineer — Motherson Sumi, Gurgaon (Jun 2021 – Present)\n • Managing QA for automotive wiring harnesses serving Maruti and Honda.\n • Led IATF 16949 certification with zero major non-conformances.\n • Reduced PPM from 450 to 85 through 8D problem-solving.\n\nQuality Engineer — Lumax Industries, Gurgaon (Aug 2018 – May 2021)\n\nEDUCATION\nB.Tech Mechanical — DTU, Delhi, 2018\n\nSKILLS\nIATF 16949, PPAP, FMEA, APQP, SPC, MSA, 8D, CMM, GD&T`,
senior: `Ashish Khandelwal — VP Quality & Engineering\nPune | ashish.k@email.com\n\nSUMMARY\nVP Quality with 16 years in automotive OEM and Tier-1 quality management. Led quality functions for plants producing 500K+ vehicles annually.\n\nEXPERIENCE\nVP Quality — Tata Motors, Pune (Jan 2017 – Present)\n • Leading quality function for passenger vehicle division with 3 manufacturing plants.\n • Reduced warranty claims by 35% through design-of-experiments and field failure analysis.\n • Implemented World Class Manufacturing (WCM) quality pillar across all plants.\n\nQuality Head — Bosch India, Bangalore (Jul 2011 – Dec 2016)\n\nEDUCATION\nM.Tech Quality Engineering — IIT Delhi, 2008\nSix Sigma Master Black Belt`,
jd: `Quality Engineer — Maruti Suzuki, Gurgaon\n\nRequirements:\n • 3+ years in automotive quality\n • Knowledge of IATF 16949, PPAP, APQP, FMEA\n • Experience with 8D problem-solving\n • CMM and GD&T proficiency`
},

"Aerospace": {
entry: `Harish Kumar — Aerospace Trainee Engineer\nBangalore | harish.k@email.com\n\nSUMMARY\nM.Tech Aerospace graduate with thesis in computational fluid dynamics. Familiar with ANSYS Fluent and wind tunnel testing. Interned at HAL.\n\nEDUCATION\nM.Tech Aerospace — IIT Kanpur, 2024\n\nTHESIS\nCFD analysis of transonic flow over a NACA 0012 airfoil using ANSYS Fluent. Validated results against wind tunnel data with <5% error.\n\nINTERNSHIP\nTrainee — HAL, Bangalore (May 2023 – Jul 2023)\n • Assisted in structural testing of LCA Tejas wing components.\n\nSKILLS\nANSYS Fluent, ANSYS Structural, CATIA V5, MATLAB, aerodynamics, CFD, structural analysis basics`,
mid: `Tanvi Kulkarni — Stress Engineer\nBangalore | tanvi.kulkarni@email.com\n\nSUMMARY\nAerospace stress analyst with 4 years in structural analysis of aircraft components using FEA per FAR/CS-25 regulations.\n\nEXPERIENCE\nStress Engineer — HAL, Bangalore (Jun 2021 – Present)\n • Performing stress analysis of wing structures for LCA Tejas using MSC Nastran and Patran.\n • Conducting damage tolerance analysis per DGCA requirements.\n • Preparing stress reports with margin of safety calculations.\n\nStress Analyst — Airbus India, Bangalore (Aug 2019 – May 2021)\n\nEDUCATION\nM.Tech Aerospace Structures — IISc Bangalore, 2019\n\nSKILLS\nMSC Nastran/Patran, ABAQUS, CATIA V5, stress analysis, damage tolerance, composite laminates, FAR/CS-25`,
senior: `Dr. Suresh Nair — Chief Structures Engineer\nBangalore | suresh.nair@email.com\n\nSUMMARY\nChief Structures Engineer with 18 years in aerospace structural design and certification. Led structural certification of 2 military aircraft programs.\n\nEXPERIENCE\nChief Structures — HAL, Bangalore (Jan 2016 – Present)\n • Leading the structures division of 60+ engineers for LCA Tejas Mk2 program.\n • Directed complete structural certification campaign for Tejas Mk1A with CEMILAC.\n • Published 20+ internal research reports on composite damage tolerance methodologies.\n\nSenior Stress Lead — Boeing India, Bangalore (Jul 2010 – Dec 2015)\n\nEDUCATION\nPh.D. Aerospace Structures — IISc Bangalore, 2006`,
jd: `Stress Engineer — Boeing India, Bangalore\n\nRequirements:\n • 3+ years aerospace structural analysis\n • Proficiency in Nastran, ABAQUS, or ANSYS\n • Knowledge of airworthiness regulations (FAR-25, CS-25)\n • Experience with composite and metallic structures`
},

"Education / Teaching": {
entry: `Ankita Srivastava — Lecturer (Fresher)\nJaipur | ankita.s@email.com\n\nSUMMARY\nM.Sc Mathematics graduate with NET qualification. 6 months of teaching experience as a guest lecturer. Strong in calculus, linear algebra, and numerical methods.\n\nEDUCATION\nM.Sc Mathematics — University of Rajasthan, 2024 (Gold Medal)\n\nNet Qualified — UGC NET Mathematics, 2024\n\nTEACHING EXPERIENCE\nGuest Lecturer — Government Engineering College, Jaipur (Jan 2024 – Jun 2024)\n • Taught Engineering Mathematics I to 120 first-year students.\n • Conducted tutorials and doubt-clearing sessions.\n\nSKILLS\nCalculus, linear algebra, differential equations, MATLAB, LaTeX, classroom teaching, question paper setting`,
mid: `Sunita Joshi — Assistant Professor\nJaipur | sunita.joshi@email.com\n\nSUMMARY\nMathematics educator with 6 years of teaching at UG and PG levels. Published 5 papers. Consistently received student feedback above 4.2/5.\n\nEXPERIENCE\nAssistant Professor — Manipal University Jaipur (Aug 2020 – Present)\n • Teaching Calculus, Linear Algebra, and Probability to 200+ students per semester.\n • Mentored 8 M.Sc. dissertation students.\n • Organized a 3-day national workshop with 80+ participants.\n\nLecturer — Government Engineering College, Ajmer (Jun 2017 – Jul 2020)\n\nEDUCATION\nPh.D. Mathematics — University of Rajasthan, 2022\nM.Sc Mathematics — Gold Medalist\n\nPUBLICATIONS\n5 papers in peer-reviewed journals (2 SCI indexed)`,
senior: `Prof. R.K. Sharma — Professor & Dean of Sciences\nDelhi | rk.sharma@email.com\n\nSUMMARY\nProfessor with 22 years of teaching and research. Published 45+ papers. Guided 8 Ph.D. students. Served as Head of Department and Dean.\n\nEXPERIENCE\nProfessor & Dean — IIT Delhi (Aug 2012 – Present)\n • Teaching advanced courses in functional analysis, topology, and numerical methods.\n • Guided 8 Ph.D. students (all completed), 25+ M.Tech dissertations.\n • Principal investigator for 5 DST/SERB funded projects totaling INR 2Cr.\n\nAssociate Professor — University of Delhi (Jul 2005 – Jul 2012)\nAssistant Professor — BHU, Varanasi (Jul 2002 – Jun 2005)\n\nEDUCATION\nPh.D. Mathematics — IIT Kanpur, 2002\n\nPUBLICATIONS\n48 papers, h-index: 15, citations: 800+`,
jd: `Assistant Professor (Mathematics) — VIT University\n\nRequirements:\n • Ph.D. in Mathematics (completed or thesis submitted)\n • 3+ years teaching experience at university level\n • Research publications in peer-reviewed journals\n • NET/SLET qualification`
},

"Research / Academia": {
entry: `Nandini K — Research Assistant\nBangalore | nandini.k@email.com\n\nSUMMARY\nM.Sc Physics graduate starting a Ph.D. in materials science. 1 year of research experience as a project assistant. Co-authored 1 paper.\n\nEDUCATION\nM.Sc Physics — IIT Madras, 2024\n\nRESEARCH\nProject Assistant — IISc Bangalore (Jul 2023 – Jun 2024)\n • Deposited ZnO thin films using RF sputtering and characterized using XRD and SEM.\n • Co-authored 1 paper in Journal of Materials Science.\n\nSKILLS\nThin film deposition, XRD, SEM, UV-Vis spectroscopy, MATLAB, Origin Pro, scientific writing`,
mid: `Dr. Ravi Shankar — Post-Doctoral Researcher\nKanpur | ravi.shankar@email.com\n\nSUMMARY\nMaterials scientist with 3 years post-doc and 4 years doctoral experience. Published 12 papers with h-index of 8. Managing a DST-funded project.\n\nEXPERIENCE\nPost-Doc — IIT Kanpur (Sep 2021 – Present)\n • Leading a DST-SERB funded project (INR 40L) on ZnO thin films for solar cells.\n • Supervising 2 Ph.D. students and 4 M.Tech students.\n\nDoctoral Research — IIT Bombay (Jul 2017 – Aug 2021)\n • Published 8 papers in Thin Solid Films and Applied Surface Science.\n\nEDUCATION\nPh.D. Materials Science — IIT Bombay, 2021\n\nPUBLICATIONS\n12 papers, h-index: 8, citations: 180+`,
senior: `Prof. Meena Gupta — Distinguished Professor\nDelhi | meena.gupta@email.com\n\nSUMMARY\nDistinguished Professor with 25 years of research in nanomaterials. Published 120+ papers with h-index 35. Fellow of Indian National Science Academy. Mentored 15 Ph.D. students.\n\nEXPERIENCE\nDistinguished Professor — IIT Delhi (Jan 2010 – Present)\n • Leading a 20-person research group in nanomaterials for energy applications.\n • Total research funding of INR 15Cr from DST, SERB, DRDO, and industry.\n • Editor-in-Chief of Journal of Nanomaterials Research.\n\nProfessor — IISc Bangalore (Jul 2005 – Dec 2009)\n\nEDUCATION\nPh.D. Physics — Cambridge University, 1999\n\nPUBLICATIONS\n125 papers, h-index: 35, 4500+ citations, 3 books`,
jd: `Research Scientist — IISc Bangalore\n\nRequirements:\n • Ph.D. in Materials Science or Physics\n • Post-doctoral experience preferred\n • Expertise in thin film deposition techniques\n • Strong publication record`
},

"Law / Legal": {
entry: `Sahil Mathur — Junior Associate\nDelhi | sahil.mathur@email.com\n\nSUMMARY\nLLB graduate from NLU with 6 months of internship experience in corporate law. Assisted in drafting contracts and conducting legal research.\n\nEDUCATION\nB.A. LL.B. — NLU Delhi, 2024\nBar Council Registration (2024)\n\nINTERNSHIPS\n • Khaitan & Co, Mumbai (2 months): Assisted in M&A due diligence and contract review.\n • District Court, Delhi (1 month): Observed civil and criminal proceedings.\n\nSKILLS\nLegal research, contract drafting, corporate law basics, SCC Online, Manupatra, legal writing`,
mid: `Adv. Pooja Mehta — Corporate Lawyer\nMumbai | pooja.mehta@email.com\n\nSUMMARY\nCorporate lawyer with 5 years in M&A transactions, contract drafting, and regulatory compliance. Handled deals worth INR 500Cr+.\n\nEXPERIENCE\nSenior Associate — AZB & Partners, Mumbai (Jan 2021 – Present)\n • Advising on 10+ M&A transactions with deal values up to INR 200Cr.\n • Drafting SaaS agreements, licensing deals, vendor contracts, and NDAs.\n • Conducting legal due diligence for PE/VC investment rounds.\n\nAssociate — Khaitan & Co, Mumbai (Jul 2018 – Dec 2020)\n\nEDUCATION\nLL.B. — NLSIU Bangalore, 2018`,
senior: `Raghav Sharma — Managing Partner\nDelhi | raghav.sharma@email.com\n\nSUMMARY\nManaging Partner with 18 years of corporate and M&A practice. Led 100+ M&A transactions totaling $5B+. Ranked by Chambers & Partners and Legal 500.\n\nEXPERIENCE\nManaging Partner — Trilegal, Delhi (Jan 2015 – Present)\n • Leading the firm's M&A and PE practice with a team of 30+ lawyers.\n • Advised on landmark deals including cross-border mergers and hostile takeovers.\n • Ranked Band 1 by Chambers Asia Pacific for Corporate/M&A.\n\nPartner — AZB & Partners (Jul 2009 – Dec 2014)\nSenior Associate — Amarchand Mangaldas (Jul 2006 – Jun 2009)\n\nEDUCATION\nLL.B. — NLS Bangalore, 2006\nLL.M. — Harvard Law School, 2010`,
jd: `Corporate Associate — Cyril Amarchand, Delhi\n\nRequirements:\n • 4+ years corporate law experience in top-tier firm\n • Experience in M&A and PE/VC transactions\n • Proficiency in contract drafting\n • Knowledge of Companies Act, FEMA, SEBI`
},

"Journalism / Media": {
entry: `Aakash Gupta — Junior Reporter\nDelhi | aakash.gupta@email.com\n\nSUMMARY\nJournalism graduate with internship at a digital news outlet. Published 30+ articles during a 4-month internship covering local politics and education.\n\nEDUCATION\nM.A. Journalism — IIMC, New Delhi, 2024\n\nINTERNSHIP\nReporter Intern — The Wire, Delhi (Mar 2024 – Jun 2024)\n • Published 30+ articles on education policy and local governance.\n • Conducted 15 interviews with teachers, parents, and officials.\n • Fact-checked 20+ news stories using government databases and RTI data.\n\nSKILLS\nNews reporting, fact-checking, interviewing, WordPress, social media, RTI applications, feature writing`,
mid: `Shreya Kapoor — Senior Reporter\nNew Delhi | shreya.kapoor@email.com\n\nSUMMARY\nJournalist with 4 years covering politics and public policy for national news outlets. Published 300+ articles with 500K+ monthly readership.\n\nEXPERIENCE\nSenior Reporter — The Indian Express, New Delhi (Feb 2022 – Present)\n • Covering Union government policy and parliamentary sessions.\n • Published a 5-part investigative series cited in a PIL before the Allahabad High Court.\n\nReporter — Scroll.in, Delhi (Jun 2019 – Jan 2022)\n • Covered 4 state election campaigns.\n\nEDUCATION\nM.A. Journalism — IIMC, New Delhi, 2019`,
senior: `Supriya Sharma — Editor-in-Chief\nMumbai | supriya.sharma@email.com\n\nSUMMARY\nEditor-in-Chief with 16 years in journalism. Led newsrooms of 50+ journalists. Won 3 national press awards. Covered international stories from 15 countries.\n\nEXPERIENCE\nEditor-in-Chief — Scroll.in (Jan 2018 – Present)\n • Leading a 55-person editorial team covering politics, economy, culture, and investigations.\n • Grew monthly readership from 5M to 25M unique visitors.\n • Won Ramnath Goenka Award for investigative journalism (2020).\n\nAssistant Editor — Hindustan Times, Delhi (Jul 2011 – Dec 2017)\n\nEDUCATION\nM.A. Journalism — Columbia University, 2008`,
jd: `Reporter — NDTV, New Delhi\n\nRequirements:\n • 3+ years in news journalism\n • Proven published article portfolio\n • Strong fact-checking and writing skills\n • Experience in politics or governance beats`
},

"Content Writing": {
entry: `Isha Malhotra — Content Writer (Fresher)\nBangalore | isha.m@email.com\n\nSUMMARY\nEnglish literature graduate with freelance writing experience. Published 20+ blog posts on Medium with 10K+ total reads. Strong command of grammar and SEO basics.\n\nEDUCATION\nM.A. English Literature — Bangalore University, 2024\n\nFREELANCE\n • Published 25 articles on Medium covering book reviews, productivity, and technology topics.\n • Wrote 10 product descriptions for a small e-commerce client.\n\nSKILLS\nContent writing, blogging, SEO basics, WordPress, Grammarly, copywriting fundamentals, social media content`,
mid: `Rohit Khanna — Content Strategist\nBangalore | rohit.khanna@email.com\n\nSUMMARY\nContent strategist with 4 years in B2B SaaS content marketing. Written 200+ articles driving 2M+ organic page views.\n\nEXPERIENCE\nSenior Content Writer — Zoho Corporation, Chennai (Apr 2021 – Present)\n • Writing 2-3 long-form blog posts per week on CRM and business productivity topics.\n • Created pillar-cluster strategy growing organic traffic from 80K to 250K monthly sessions.\n • Produced 15 customer case studies and 5 whitepapers.\n\nContent Writer — ContentStack Media, Bangalore (Jun 2019 – Mar 2021)\n\nEDUCATION\nM.A. English — Bangalore University, 2019\n\nSKILLS\nContent strategy, SEO writing, case studies, whitepapers, WordPress, Ahrefs, SEMrush`,
senior: `Priya Desai — Head of Content\nMumbai | priya.desai@email.com\n\nSUMMARY\nHead of Content with 12 years leading content teams for B2B and B2C brands. Built content operations generating 10M+ monthly organic visits and contributing to $30M annual pipeline.\n\nEXPERIENCE\nHead of Content — Freshworks, Chennai (Jun 2019 – Present)\n • Leading a 20-person content team spanning blog, SEO, video, podcast, and documentation.\n • Grew organic blog traffic from 500K to 4M monthly visits in 4 years.\n • Built content-led lead generation engine contributing 35% of MQL pipeline.\n\nContent Director — HubSpot (APAC), Singapore (Jul 2014 – May 2019)\n\nEDUCATION\nMBA Marketing — ISB Hyderabad, 2012`,
jd: `Content Writer — HubSpot, Remote\n\nRequirements:\n • 3+ years B2B content writing experience\n • Portfolio of published long-form articles\n • SEO best practices knowledge\n • Experience writing case studies or whitepapers`
},

"Graphic Design": {
entry: `Sakshi Mehta — Graphic Design Trainee\nMumbai | sakshi.mehta@email.com\n\nSUMMARY\nDesign graduate with portfolio of 20+ projects including brand identities, posters, and social media creatives. Proficient in Adobe Photoshop and Illustrator.\n\nEDUCATION\nBachelor of Design — MIT Institute of Design, Pune, 2024\n\nINTERNSHIP\nDesign Intern — Dentsu Creative, Mumbai (Feb 2024 – May 2024)\n • Created 40+ social media graphics for 2 brand accounts.\n • Assisted senior designers in preparing print-ready artwork for brochures.\n\nSKILLS\nAdobe Photoshop, Illustrator, InDesign, Figma, typography basics, brand identity, social media design`,
mid: `Anisha Roy — Senior Graphic Designer\nMumbai | anisha.roy@email.com\n\nSUMMARY\nGraphic designer with 5 years in branding, print design, and digital media. Designed visual identities for 20+ brands. Won packaging design award.\n\nEXPERIENCE\nSenior Graphic Designer — Ogilvy India, Mumbai (Mar 2021 – Present)\n • Leading visual design for 4 major brand accounts.\n • Won India Packaging Award 2023 (Silver) for FMCG product line.\n • Creating 50+ social media assets per month.\n\nGraphic Designer — WPP India, Mumbai (Jul 2018 – Feb 2021)\n\nEDUCATION\nB.Des Communication Design — NID Ahmedabad, 2018\n\nSKILLS\nAdobe CS (Photoshop, Illustrator, InDesign, After Effects), Figma, typography, branding, packaging, motion graphics`,
senior: `Rajesh Shinde — Creative Director\nMumbai | rajesh.shinde@email.com\n\nSUMMARY\nCreative Director with 14 years leading brand design at top agencies. Managed teams of 15+ designers. Won 25+ national and international design awards.\n\nEXPERIENCE\nCreative Director — Leo Burnett India, Mumbai (Jan 2018 – Present)\n • Leading the design studio of 18 designers servicing 10 major brand accounts.\n • Won 8 Cannes Lions and 15 Kyoorius Design Awards.\n • Directed complete brand overhauls for 3 Fortune 500 clients.\n\nSenior Art Director — JWT India (Jul 2012 – Dec 2017)\n\nEDUCATION\nM.Des — NID Ahmedabad, 2010`,
jd: `Graphic Designer — Dentsu Creative, Bangalore\n\nRequirements:\n • 3+ years professional graphic design experience\n • Mastery of Adobe Photoshop, Illustrator, InDesign\n • Strong portfolio in branding and digital design\n • Understanding of typography and color theory`
},

"UI/UX Design": {
entry: `Meghna Nair — UX Design Intern\nBangalore | meghna.nair@email.com\n\nSUMMARY\nM.Des Interaction Design graduate with 3 portfolio projects demonstrating user research, wireframing, and prototyping. Proficient in Figma.\n\nEDUCATION\nM.Des Interaction Design — NID Ahmedabad, 2024\n\nPROJECTS\n • Food Delivery App Redesign: Conducted user interviews, created persona maps, and redesigned the checkout flow reducing steps from 5 to 3.\n • Banking Dashboard: Designed a municipal tax payment dashboard with user testing and 3 iteration rounds.\n\nSKILLS\nFigma, wireframing, prototyping, user research, usability testing, information architecture`,
mid: `Varun Nambiar — UX Designer\nBangalore | varun.nambiar@email.com\n\nSUMMARY\nUX designer with 4 years designing mobile apps and web applications. Conducted 50+ user research sessions. Improved onboarding completion from 45% to 72%.\n\nEXPERIENCE\nSenior UX Designer — PhonePe, Bangalore (Jan 2022 – Present)\n • Designing interfaces for the merchant app used by 15M+ merchants.\n • Conducted 25+ user research sessions with merchants in tier-2 cities.\n • Improved onboarding completion from 45% to 72%.\n\nUX Designer — Swiggy, Bangalore (Jun 2019 – Dec 2021)\n\nEDUCATION\nM.Des — IDC, IIT Bombay, 2019\n\nSKILLS\nFigma, Sketch, user research, usability testing, wireframing, prototyping, design systems, accessibility`,
senior: `Ashwini Deshpande — VP Design\nBangalore | ashwini.d@email.com\n\nSUMMARY\nVP Design with 13 years leading design teams at consumer internet companies. Built and managed design teams of 25+. Shaped product design for 50M+ users.\n\nEXPERIENCE\nVP Design — CRED, Bangalore (Mar 2020 – Present)\n • Leading a 30-person design team (UX, UI, brand, research) for an app with 20M+ users.\n • Defined the design language that became CRED's signature minimalist luxury aesthetic.\n • Established the design research practice hiring 5 researchers.\n\nDesign Director — Flipkart, Bangalore (Jun 2014 – Feb 2020)\n\nEDUCATION\nM.Des — RCA London, 2011`,
jd: `UX Designer — Razorpay, Bangalore\n\nRequirements:\n • 3+ years UX/product design\n • Figma proficiency (required)\n • User research and usability testing experience\n • Strong portfolio showing end-to-end process`
},

"Animation / VFX": {
entry: `Rishi Jain — Junior Animator\nMumbai | rishi.jain@email.com\n\nSUMMARY\nAnimation graduate with a demo reel featuring character walks, run cycles, and a 30-second short film. Proficient in Maya and After Effects.\n\nEDUCATION\nB.Sc Animation & Multimedia — Arena Animation, Mumbai, 2024\n\nPROJECTS\n • 30-second character animation short film in Maya\n • Walk cycle and run cycle animations for biped and quadruped characters\n\nSKILLS\nAutodesk Maya, After Effects, Photoshop, character animation basics, 12 principles of animation`,
mid: `Kiran Rao — 3D Animator / VFX Artist\nHyderabad | kiran.rao@email.com\n\nSUMMARY\n3D animator with 4 years in character animation, motion capture cleanup, and VFX for feature films. Worked on 3 feature films and 2 OTT series.\n\nEXPERIENCE\nSenior 3D Animator — DNEG India, Hyderabad (Feb 2022 – Present)\n • Animating character performances for VFX feature films in Maya.\n • Cleaned up motion capture data using MotionBuilder.\n • Polished 40+ shots for a Marvel project.\n\nJunior Animator — Technicolor India, Chennai (Jul 2019 – Jan 2022)\n\nSKILLS\nMaya, Houdini, MotionBuilder, ZBrush, Nuke, character animation, motion capture`,
senior: `Pradeep Sharma — Animation Supervisor\nMumbai | pradeep.sharma@email.com\n\nSUMMARY\nAnimation Supervisor with 14 years in feature film VFX. Supervised animation on 10+ international feature films including 3 Marvel projects. Managed teams of 40+ animators.\n\nEXPERIENCE\nAnimation Supervisor — Framestore India, Mumbai (Jan 2018 – Present)\n • Supervising a team of 45 animators working on tent-pole VFX films.\n • Led creature animation for 2 Marvel films, earning VES nomination.\n • Developed internal animation training curriculum used across all Framestore studios.\n\nLead Animator — DNEG, Mumbai (Jul 2012 – Dec 2017)\n\nEDUCATION\nDiploma in Animation — Vancouver Film School, 2010`,
jd: `3D Animator — Prime Focus, Mumbai\n\nRequirements:\n • 3+ years 3D character animation\n • Proficiency in Maya\n • Understanding of animation principles\n • Strong demo reel`
},

"Film / Entertainment": {
entry: `Arjun Mehta — Assistant Director Trainee\nMumbai | arjun.mehta@email.com\n\nSUMMARY\nFTII graduate with experience as a second AD on 2 short films and 1 ad film. Familiar with scheduling, call sheets, and on-set coordination.\n\nEDUCATION\nDiploma in Film Direction — FTII Pune, 2024\n\nEXPERIENCE\n • Second AD on 2 short films (15-20 min each) and 1 commercial ad film.\n • Prepared daily call sheets, managed extras, and coordinated art department logistics.\n\nSKILLS\nFilm direction, call sheet preparation, scheduling, script breakdown, on-set coordination`,
mid: `Nisha Varma — First AD / Line Producer\nMumbai | nisha.varma@email.com\n\nSUMMARY\nFilm professional with 5 years as AD and line producer. Managed production for 3 feature films and 4 web series. Budgets up to INR 30Cr.\n\nEXPERIENCE\nFirst AD — Dharma Productions, Mumbai (Jan 2022 – Present)\n • First AD on a theatrical release (INR 30Cr budget), crew of 150+, 60-day shoot.\n • Managing location permits, vendor contracts, and production budgets within 5% variance.\n\nSecond AD — Excel Entertainment (May 2019 – Dec 2021)\n\nEDUCATION\nDiploma in Direction — FTII Pune, 2019`,
senior: `Anil Kapoor — Executive Producer\nMumbai | anil.k@email.com\n\nSUMMARY\nExecutive Producer with 16 years in film and OTT production. Produced 12 feature films and 8 web series with combined box office of INR 800Cr+.\n\nEXPERIENCE\nEP — Netflix India, Mumbai (Jun 2019 – Present)\n • Overseeing production of 6-8 original series annually with combined budgets of INR 400Cr.\n • Greenlit and shepherded 3 critically acclaimed original series.\n\nProducer — Excel Entertainment (Jul 2011 – May 2019)\n\nEDUCATION\nMBA Entertainment — USC School of Cinematic Arts, 2008`,
jd: `Line Producer — YRF, Mumbai\n\nRequirements:\n • 4+ years in film production\n • Experience managing large crews\n • Production budgeting and scheduling\n • Location permits and regulatory knowledge`
},

"Hospitality / Hotel Management": {
entry: `Riya George — Front Desk Trainee\nGoa | riya.george@email.com\n\nSUMMARY\nHotel Management graduate with 6-month industrial training at a 5-star resort. Trained in front desk operations, guest handling, and Food & Beverage service.\n\nEDUCATION\nB.Sc Hotel Management — IHM Goa, 2024\n\nINDUSTRIAL TRAINING\nManagement Trainee — Taj Hotels, Goa (Jan 2024 – Jun 2024)\n • Rotated through front desk, housekeeping, F&B, and banquets departments.\n • Handled 50+ guest check-ins and check-outs using Opera PMS.\n\nSKILLS\nFront desk operations, Opera PMS basics, guest relations, F&B service, telephone etiquette`,
mid: `Ashwin Thomas — Front Office Manager\nGoa | ashwin.thomas@email.com\n\nSUMMARY\nHotel management professional with 6 years in front office operations. Managed teams at 200+ room 5-star properties. Guest satisfaction 4.6/5 on TripAdvisor.\n\nEXPERIENCE\nFront Office Manager — Taj Hotels, Goa (Mar 2021 – Present)\n • Managing 15 front desk staff at a 250-room resort.\n • Maintained 92% occupancy during peak season.\n • Implemented digital check-in reducing time from 8 to 3 minutes.\n\nFront Desk Supervisor — ITC Hotels, Chennai (Jun 2018 – Feb 2021)\n\nEDUCATION\nB.Sc Hotel Management — IHM Goa, 2018`,
senior: `Sanjay Nair — General Manager\nMumbai | sanjay.nair@email.com\n\nSUMMARY\nGM with 18 years in luxury hospitality. Managed 5-star hotels with 300-500 rooms. Grew RevPAR by 25% across 3 properties. TripAdvisor Travelers Choice winner.\n\nEXPERIENCE\nGeneral Manager — Oberoi Hotels, Mumbai (Jan 2018 – Present)\n • Managing a 350-room luxury hotel with 500+ staff and INR 200Cr annual revenue.\n • Increased RevPAR from INR 8,500 to INR 12,000 through yield management.\n • Led INR 50Cr hotel renovation project completing on time and on budget.\n\nResident Manager — Taj Mumbai (Jul 2011 – Dec 2017)\n\nEDUCATION\nMBA Hospitality — Cornell University, 2008`,
jd: `Front Office Manager — Marriott Hotels, Mumbai\n\nRequirements:\n • 5+ years front office experience in 4/5-star hotels\n • Opera PMS proficiency\n • Team management (10+ people)\n • Revenue management knowledge`
},

"Tourism / Travel": {
entry: `Divya Chandra — Travel Executive Trainee\nDelhi | divya.chandra@email.com\n\nSUMMARY\nBBA Tourism graduate with internship in tour operations. Processed 100+ booking requests during internship. Familiar with GDS basics.\n\nEDUCATION\nBBA Tourism — Amity University, 2024\n\nINTERNSHIP\nTravel Intern — Thomas Cook India, Delhi (Mar 2024 – Jun 2024)\n • Assisted in processing domestic tour bookings for 100+ customers.\n • Learned Amadeus GDS basics for flight searches and reservations.\n\nSKILLS\nTour operations basics, Amadeus basics, itinerary planning, customer service, MS Office`,
mid: `Prerna Malik — Travel Operations Manager\nDelhi | prerna.malik@email.com\n\nSUMMARY\nTravel professional with 5 years organizing 200+ group tours. Managed vendor relationships and MICE events.\n\nEXPERIENCE\nOperations Manager — Thomas Cook India, Delhi (May 2021 – Present)\n • Managing 100+ group tours annually covering SE Asia, Europe, and domestic destinations.\n • Negotiated rates with 40+ vendors, achieving 15% cost savings.\n • Designed itineraries for MICE events with budgets up to INR 1Cr.\n\nTravel Executive — MakeMyTrip, Gurgaon (Jul 2018 – Apr 2021)\n\nSKILLS\nTour operations, itinerary design, GDS (Amadeus, Galileo), vendor management, MICE`,
senior: `Suresh Menon — CEO, Travel Company\nMumbai | suresh.menon@email.com\n\nSUMMARY\nCEO with 16 years in travel industry. Built a travel company from scratch to INR 100Cr revenue. Managed 200+ employees and operations across 5 countries.\n\nEXPERIENCE\nCEO — Traveazy (Own Company), Mumbai (Jan 2016 – Present)\n • Founded and scaled a B2B travel platform to INR 100Cr revenue and 200+ employees.\n • Partnered with 500+ hotels and 50+ airlines across 20 countries.\n\nVP Operations — Cox & Kings, Mumbai (Jul 2010 – Dec 2015)\n\nEDUCATION\nMBA — IIM Kozhikode, 2008`,
jd: `Travel Operations Manager — SOTC Travel, Mumbai\n\nRequirements:\n • 4+ years in travel operations\n • GDS knowledge (Amadeus, Galileo)\n • Vendor management skills\n • MICE experience preferred`
},

"Retail / E-commerce": {
entry: `Amrita Sen — Retail Analyst Trainee\nBangalore | amrita.sen@email.com\n\nSUMMARY\nMBA Retail Management fresher with internship in e-commerce category management. Assisted in product listing optimization and sales data analysis.\n\nEDUCATION\nMBA Retail Management — NIFT, Mumbai, 2024\n\nINTERNSHIP\nCategory Intern — Flipkart, Bangalore (Apr 2024 – Jul 2024)\n • Assisted in managing product listings for 500+ SKUs in kitchen category.\n • Created weekly Excel reports analyzing category conversion rates and returns data.\n\nSKILLS\nRetail basics, Excel (pivot tables), SQL basics, e-commerce metrics, category management concepts`,
mid: `Pallavi Sharma — Category Manager\nBangalore | pallavi.s@email.com\n\nSUMMARY\nE-commerce professional with 4 years in category management. Managed electronics category with INR 120Cr annual GMV.\n\nEXPERIENCE\nCategory Manager — Flipkart, Bangalore (Jun 2021 – Present)\n • Managing small appliances category with 5000+ SKUs and INR 120Cr GMV.\n • Onboarded 30+ new sellers, growing selection by 40%.\n • Designed Big Billion Days campaigns achieving 3x normal GMV.\n\nMarketplace Associate — Amazon India (Jul 2019 – May 2021)\n\nEDUCATION\nMBA Retail — NIFT Mumbai, 2019\n\nSKILLS\nCategory management, P&L, marketplace operations, Excel, SQL, pricing strategy`,
senior: `Raghunath Goyal — VP E-commerce\nBangalore | raghunath.g@email.com\n\nSUMMARY\nVP E-commerce with 14 years building and scaling online retail businesses. Managed P&L of INR 5000Cr+ GMV. Led 100+ person teams.\n\nEXPERIENCE\nVP E-commerce — Reliance Retail, Mumbai (Jun 2019 – Present)\n • Leading JioMart e-commerce operations across 200+ cities with INR 5000Cr annual GMV.\n • Scaled from 50 cities to 200+ cities in 3 years with same-day delivery capability.\n\nDirector — Amazon India, Hyderabad (Jul 2013 – May 2019)\n\nEDUCATION\nMBA — IIM Calcutta, 2010`,
jd: `Category Manager — Myntra, Bangalore\n\nRequirements:\n • 3+ years e-commerce category management\n • Strong analytical skills (Excel, SQL)\n • Experience with marketplace operations\n • Understanding of e-commerce metrics`
},

"Customer Support": {
entry: `Prashanth M — Customer Support Executive\nHyderabad | prashanth.m@email.com\n\nSUMMARY\nB.Tech graduate with 3 months of customer support internship. Handled 30+ tickets daily via email and chat. Trained on Freshdesk ticketing system.\n\nEDUCATION\nB.Tech IT — JNTU Hyderabad, 2024\n\nINTERNSHIP\nSupport Intern — Freshworks, Chennai (Apr 2024 – Jun 2024)\n • Resolved 30+ customer tickets daily via email and chat.\n • Created 5 knowledge base article drafts for common issues.\n\nSKILLS\nCustomer support, Freshdesk basics, email communication, chat support, technical troubleshooting basics`,
mid: `Ravi Teja — Support Team Lead\nHyderabad | ravi.teja@email.com\n\nSUMMARY\nSupport professional with 5 years handling B2B SaaS support. Led team of 12. CSAT 93%, first-response <2 minutes.\n\nEXPERIENCE\nTeam Lead — Freshworks, Hyderabad (Apr 2021 – Present)\n • Leading 12 agents handling 500+ tickets daily.\n • CSAT 93%, first-response 1.8 minutes.\n • Created 50+ knowledge base articles reducing repeat tickets by 25%.\n\nSupport Executive — Zendesk, Hyderabad (Jun 2018 – Mar 2021)\n\nSKILLS\nFreshdesk, Zendesk, Intercom, live chat, technical troubleshooting, team management, knowledge base`,
senior: `Meghana Rao — VP Customer Success\nBangalore | meghana.rao@email.com\n\nSUMMARY\nVP Customer Success with 12 years building support and CS organizations. Managed 80+ person teams. Reduced churn by 30% through proactive CS programs.\n\nEXPERIENCE\nVP Customer Success — Chargebee, Chennai (Jun 2019 – Present)\n • Leading CS, support, and onboarding teams (85 people) for 4500+ enterprise customers.\n • Reduced logo churn from 8% to 5.5% through health scoring and proactive engagement.\n • Built the customer onboarding team from scratch, reducing time-to-value from 45 days to 15 days.\n\nDirector Support — Zoho, Chennai (Jul 2012 – May 2019)\n\nEDUCATION\nMBA — Great Lakes, Chennai, 2012`,
jd: `Support Lead — Chargebee, Chennai\n\nRequirements:\n • 4+ years SaaS customer support\n • Team leadership experience\n • Helpdesk tools (Freshdesk, Zendesk)\n • Technical troubleshooting ability`
},

"Public Administration": {
entry: `Ankur Singh — IAS Probationer\nMussorie | ankur.singh@email.com\n\nSUMMARY\nIAS officer (2023 batch) undergoing foundation training at LBSNAA. Topped district-level UPSC study group. Background in political science.\n\nEDUCATION\nIAS — UPSC CSE 2023 (AIR 120)\nM.A. Political Science — JNU, 2021\n\nTRAINING\nLBSNAA Foundation Course (ongoing) — Village attachment, district attachment, Bharat Darshan study tour.\n\nSKILLS\nPolicy analysis, public speaking, report writing, stakeholder management, leadership`,
mid: `Snehal Deshmukh — SDM (Sub-Divisional Magistrate)\nNagpur | snehal.d@email.com\n\nSUMMARY\nIAS officer with 4 years in district governance. Overseeing revenue administration for 800K population. Implemented welfare scheme drives.\n\nEXPERIENCE\nSDM — Nagpur Division (Oct 2021 – Present)\n • Administering 3 tehsils with 800K population.\n • Identified 4000+ ghost beneficiaries, redirecting INR 3.2Cr in welfare funds.\n • Coordinated drought relief operations.\n\nProbationary Officer — Latur District (Aug 2019 – Sep 2021)\n\nEDUCATION\nIAS — UPSC CSE 2019 (AIR 156)\nB.A. Political Science — Fergusson College, 2017`,
senior: `Rajiv Kumar — Principal Secretary\nNew Delhi | rajiv.kumar@email.com\n\nSUMMARY\nPrincipal Secretary (IAS 2000 batch) with 24 years of administrative experience. Served as District Collector, Municipal Commissioner, and PS to CM.\n\nEXPERIENCE\nPrincipal Secretary, IT — Government of Maharashtra (Jun 2020 – Present)\n • Leading digital transformation initiatives for state government with INR 500Cr budget.\n • Launched Maharashtra Seva Kendra covering 400+ government services online.\n\nMunicipal Commissioner — Pune (Jul 2016 – May 2020)\nDistrict Collector — Nashik (Jun 2012 – Jun 2016)\n\nEDUCATION\nIAS — UPSC CSE 2000 (AIR 45)\nM.Phil Public Policy — Princeton University (Mid-Career Fellowship)`,
jd: `District Program Officer — NITI Aayog\n\nRequirements:\n • 3+ years government administration experience\n • Knowledge of welfare schemes\n • Program monitoring and evaluation skills\n • Report writing and analytical skills`
},

"Government Jobs": {
entry: `Priya Kumari — Assistant Section Officer\nNew Delhi | priya.kumari@email.com\n\nSUMMARY\nSSC CGL qualified officer (2023) posted in Central Secretariat Service. Undergoing foundation training in government procedures and file management.\n\nEDUCATION\nSSC CGL — 2023 (Qualified)\nB.A. Hindi — Delhi University, 2021\n\nTRAINING\nISTM Foundation Course — Government procedures, noting and drafting, e-Office system.\n\nSKILLS\nGovernment procedures, noting and drafting basics, e-Office, MS Office, Hindi and English`,
mid: `Manoj Kumar — Section Officer\nNew Delhi | manoj.kumar@email.com\n\nSUMMARY\nGovernment officer with 8 years in Central Secretariat. Handled policy files, RTI matters, and inter-ministerial coordination.\n\nEXPERIENCE\nSection Officer — Ministry of Commerce (Apr 2020 – Present)\n • Managing Trade Policy section with 200+ files monthly.\n • Coordinating inter-ministerial consultations for Foreign Trade Policy.\n • Processing 50+ RTI applications monthly with 100% compliance.\n\nASO — Ministry of Education (Jun 2015 – Mar 2020)\n\nEDUCATION\nSSC CGL — 2015 (AIR 89)\nM.A. Public Administration — IGNOU, 2018`,
senior: `S.K. Mishra — Additional Secretary\nNew Delhi | sk.mishra@email.com\n\nSUMMARY\nAdditional Secretary with 28 years of government service. Served in 5 ministries including Finance, Commerce, and Defence. Led policy reforms impacting 100M+ citizens.\n\nEXPERIENCE\nAdditional Secretary — Ministry of Finance (Jan 2020 – Present)\n • Leading GST policy division, contributing to simplification of GST compliance for 14M+ taxpayers.\n • Coordinated the Union Budget preparation process for 2 consecutive fiscal years.\n\nJoint Secretary — Ministry of Commerce (Jul 2015 – Dec 2019)\n\nEDUCATION\nIAS — UPSC 1996 batch\nM.Phil Economics — DSE, Delhi University`,
jd: `Deputy Secretary — DoPT, New Delhi\n\nRequirements:\n • 8+ years government service\n • Policy formulation experience\n • Government noting and drafting proficiency\n • e-Office and digital governance experience`
},

"Defense / Military": {
entry: `Lt. Arun Sharma — Army Officer\nDehradun | arun.sharma@email.com\n\nSUMMARY\nLieutenant in the Indian Army (2023 commission). Completed IMA training. Currently posted in an infantry battalion. Trained in weapons handling, tactics, and leadership.\n\nEDUCATION\nIMA Dehradun — Commissioned 2023\nNDA Khadakwasla — 2020\n\nTRAINING\nYoung Officers Course — Infantry School, Mhow (2024)\n • Weapons proficiency: Assault rifles, LMGs, mortars.\n • Tactical training: Platoon-level operations, map reading, field craft.\n\nSKILLS\nMilitary leadership, weapons handling, physical fitness, tactical planning, map reading`,
mid: `Major Vikrant Singh (Retd.) — Security Consultant\nChandigarh | vikrant.singh@email.com\n\nSUMMARY\nRetired army officer with 14 years of service. Combat operations, logistics management, and security consulting experience.\n\nEXPERIENCE\nSecurity Consultant — EY India, Gurgaon (Jan 2023 – Present)\n • Providing physical security risk assessments for corporate clients.\n • Conducting business continuity planning workshops.\n\nMajor — Indian Army (Jul 2008 – Dec 2022)\n • Commanded a company of 120+ soldiers in J&K counter-insurgency operations.\n • Managed logistics for battalion of 800+ troops.\n\nEDUCATION\nNDA, Khadakwasla, 2008\nIMA, Dehradun, 2009\nMBA Operations — Symbiosis (Distance), 2020\n\nCERTIFICATIONS\nCPP — ASIS International`,
senior: `Lt. Gen. R.S. Grewal (Retd.) — Defense Advisor\nNew Delhi | rs.grewal@email.com\n\nSUMMARY\nRetired Lt. General with 36 years of military service. Commanded a division of 15,000+ troops. Defense strategy advisor to government and corporate entities.\n\nEXPERIENCE\nDefense Advisor — Ministry of Defence (Consultant) (Jan 2021 – Present)\n • Advising on defense procurement modernization and strategic planning.\n\nGOC, Infantry Division — Indian Army (Jul 2017 – Dec 2020)\n • Commanding a 15,000-strong division including 3 brigades in operational area.\n\nCorps Chief of Staff (Jun 2014 – Jun 2017)\nBrigade Commander (Jul 2011 – May 2014)\n\nEDUCATION\nNDA, IMA\nHigher Command Course — Army War College, Mhow\nRCSS — Royal College of Defence Studies, London`,
jd: `Security Head — Reliance Industries, Mumbai\n\nRequirements:\n • 10+ years security management or military experience\n • Physical security systems knowledge\n • Risk assessment and BCP experience\n • Leadership and team management`
},

"Agriculture": {
entry: `Vikash Kumar — Agricultural Extension Officer Trainee\nLucknow | vikash.kumar@email.com\n\nSUMMARY\nB.Sc Agriculture graduate with field experience from rural agricultural internship. Familiar with crop cultivation, soil testing, and farmer training.\n\nEDUCATION\nB.Sc Agriculture — GBPUAT Pantnagar, 2024\n\nINTERNSHIP\nField Intern — Krishi Vigyan Kendra, Lucknow (Jan 2024 – May 2024)\n • Assisted in organizing farmer training camps for 200+ farmers on crop rotation and IPM.\n • Collected soil samples from 50+ farms for NPK analysis.\n\nSKILLS\nCrop management basics, soil testing, farmer training, field data collection, MS Excel`,
mid: `Rakesh Yadav — Agronomist / Farm Manager\nLucknow | rakesh.yadav@email.com\n\nSUMMARY\nAgronomist with 5 years managing 500+ acre commercial farms. Increased yields by 25-35% through technology-driven farming.\n\nEXPERIENCE\nFarm Manager — ITC Agri Business, Lucknow (Mar 2021 – Present)\n • Managing 600 acres of wheat, rice, and sugarcane cultivation.\n • Implemented drip irrigation, reducing water consumption by 30% while increasing yield 20%.\n • Training 150+ contract farmers on IPM and crop rotation.\n\nJunior Agronomist — Bayer CropScience (Jun 2018 – Feb 2021)\n\nEDUCATION\nM.Sc Agronomy — IARI, New Delhi, 2018`,
senior: `Dr. Ashok Dalwai — Director, Agriculture Research\nNew Delhi | ashok.dalwai@email.com\n\nSUMMARY\nDirector of Agricultural Research with 20 years in agronomy, precision agriculture, and agricultural policy. Led research programs with INR 50Cr+ funding.\n\nEXPERIENCE\nDirector — ICAR-IARI, New Delhi (Jun 2018 – Present)\n • Leading 100+ scientists in crop improvement, soil science, and agricultural engineering research.\n • Developed 5 new crop varieties registered with PPVFRA.\n • Secured INR 60Cr in research funding from DST, ICAR, and World Bank.\n\nPrincipal Scientist — ICAR-CRIDA, Hyderabad (Jul 2010 – May 2018)\n\nEDUCATION\nPh.D. Agronomy — IARI, 2004`,
jd: `Agronomist — UPL Limited, Hyderabad\n\nRequirements:\n • M.Sc in Agronomy or Soil Science\n • 3+ years field experience\n • Knowledge of crop protection products\n • Willingness to travel`
},

"Food Technology": {
entry: `Deepa Srinivasan — Food Technology Trainee\nMysore | deepa.s@email.com\n\nSUMMARY\nM.Tech Food Technology fresher from CFTRI with dissertation in dairy product development. Familiar with HACCP, food safety, and sensory evaluation.\n\nEDUCATION\nM.Tech Food Technology — CFTRI Mysore, 2024\n\nDISSERTATION\nDeveloped a probiotic yogurt with extended shelf life using encapsulated cultures. Conducted sensory evaluation with 20 panelists.\n\nSKILLS\nFood chemistry, microbiology, HACCP awareness, sensory evaluation, dairy processing, lab techniques`,
mid: `Shilpa Menon — Quality & NPD Manager\nMysore | shilpa.menon@email.com\n\nSUMMARY\nFood technologist with 5 years in product development and quality assurance. Launched 15+ food products from concept to commercial production.\n\nEXPERIENCE\nQuality Manager — Nestle India, Mysore (Feb 2021 – Present)\n • Leading NPD for confectionery, managing 5 launches per year.\n • Ensuring FSSAI compliance and HACCP/ISO 22000 standards.\n • Conducting sensory panels with 15-20 trained panelists.\n\nFood Technologist — Britannia, Bangalore (Jul 2018 – Jan 2021)\n\nEDUCATION\nM.Tech Food Technology — CFTRI Mysore, 2018`,
senior: `Dr. Rajendra Prasad — VP R&D, Foods Division\nMumbai | rajendra.prasad@email.com\n\nSUMMARY\nVP R&D with 18 years leading food product innovation for FMCG companies. Launched 100+ products generating INR 2000Cr+ in cumulative revenue.\n\nEXPERIENCE\nVP R&D — ITC Foods, Bangalore (Jan 2017 – Present)\n • Leading a 50-person R&D team for snacks, noodles, and biscuit categories.\n • Launched 30+ new products in 5 years with 80% market survival rate.\n • Built the ITC Foods Innovation Center with INR 30Cr investment.\n\nHead of R&D — Britannia Industries (Jul 2010 – Dec 2016)\n\nEDUCATION\nPh.D. Food Science — Cornell University, 2006`,
jd: `Food Technologist — Amul, Anand\n\nRequirements:\n • M.Tech in Food Technology\n • 3+ years product development or QA experience\n • HACCP and FSSAI knowledge\n • Sensory evaluation experience`
},

"Environmental Science": {
entry: `Prateek Mishra — Environmental Trainee\nPune | prateek.mishra@email.com\n\nSUMMARY\nM.Tech Environmental Engineering fresher with thesis in water quality modeling. Familiar with environmental monitoring equipment and EIA concepts.\n\nEDUCATION\nM.Tech Environmental Engineering — IIT Delhi, 2024\n\nTHESIS\nWater quality modeling of Yamuna River using QUAL2K software. Calibrated model against 12 months of field data.\n\nSKILLS\nWater quality analysis, environmental monitoring, QUAL2K, GIS basics, lab analysis, EIA concepts`,
mid: `Arun Sharma — Environmental Consultant\nPune | arun.sharma@email.com\n\nSUMMARY\nEnvironmental consultant with 5 years in EIA, pollution monitoring, and regulatory compliance. Prepared 30+ EIA reports.\n\nEXPERIENCE\nSenior Consultant — SGS India, Pune (Apr 2021 – Present)\n • Preparing EIA/EMP reports for power plants, highways, and industrial estates.\n • Conducting baseline environmental monitoring (air, water, noise, soil).\n • Coordinating public hearings with SEIAA.\n\nEnvironmental Engineer — AECOM India (Jul 2018 – Mar 2021)\n\nEDUCATION\nM.Tech Environmental — IIT Delhi, 2018`,
senior: `Dr. Sunita Narain — Director, Environmental Research\nNew Delhi | sunita.n@email.com\n\nSUMMARY\nDirector with 20 years leading environmental research and policy advocacy. Published 50+ reports on air quality, water, and climate change.\n\nEXPERIENCE\nDirector — Centre for Science & Environment, New Delhi (Jan 2012 – Present)\n • Leading a 100-person organization spanning research, policy advocacy, and environmental education.\n • Published landmark reports on urban air quality influencing National Clean Air Programme.\n • Advised Supreme Court-appointed committees on vehicular emissions and solid waste.\n\nSenior Fellow — TERI, New Delhi (Jul 2004 – Dec 2011)\n\nEDUCATION\nPh.D. Environmental Science — JNU, 2004`,
jd: `Environmental Consultant — WAPCOS, New Delhi\n\nRequirements:\n • M.Tech in Environmental Engineering\n • 3+ years EIA experience\n • Knowledge of MoEFCC guidelines\n • Environmental monitoring experience`
},

"Real Estate": {
entry: `Kunal Jain — Real Estate Sales Executive\nNoida | kunal.jain@email.com\n\nSUMMARY\nBBA graduate with 3 months of internship in residential property sales. Conducted 50+ site visits and assisted in 5 unit bookings.\n\nEDUCATION\nBBA — Amity University, 2024\n\nINTERNSHIP\nSales Intern — DLF Limited, Noida (Apr 2024 – Jun 2024)\n • Conducted 50+ customer site visits, presenting project layouts and pricing.\n • Assisted senior sales managers in preparing booking forms for 5 units.\n • Updated lead tracker in CRM with 300+ prospect records.\n\nSKILLS\nProperty sales basics, CRM basics, customer presentation, Excel, communication`,
mid: `Siddharth Jain — Real Estate Sales Manager\nNoida | siddharth.jain@email.com\n\nSUMMARY\nReal estate professional with 6 years selling 200+ residential units worth INR 150Cr+.\n\nEXPERIENCE\nSales Manager — DLF, Noida (May 2021 – Present)\n • Sold 85 units worth INR 95Cr in the first year.\n • Managing 40+ channel partners.\n • Conducting 15-20 site visits per week.\n\nSales Executive — Godrej Properties (Jun 2017 – Apr 2021)\n\nSKILLS\nProperty sales, channel partner management, Salesforce, RERA compliance`,
senior: `Ashish Puravankara — VP Sales & Marketing\nBangalore | ashish.p@email.com\n\nSUMMARY\nVP Sales with 14 years in premium real estate. Sold INR 3000Cr+ in residential projects. Built and managed sales teams of 40+ people.\n\nEXPERIENCE\nVP Sales — Prestige Group, Bangalore (Jan 2017 – Present)\n • Leading sales for 6 premium residential projects with combined inventory of INR 4000Cr.\n • Achieved 95% sell-through rate on 3 flagship projects within 18 months of launch.\n • Built a digital sales funnel contributing 40% of total leads.\n\nGM Sales — Brigade Group (Jul 2010 – Dec 2016)\n\nEDUCATION\nMBA Marketing — IIM Kozhikode, 2010`,
jd: `Sales Manager — Prestige Group, Bangalore\n\nRequirements:\n • 4+ years residential real estate sales\n • Channel partner management experience\n • CRM proficiency\n • RERA knowledge`
},

"Architecture": {
entry: `Shruti Patel — Junior Architect\nAhmedabad | shruti.patel@email.com\n\nSUMMARY\nB.Arch graduate with COA registration. Completed 6-month internship at a design firm. Proficient in AutoCAD, Revit, and SketchUp.\n\nEDUCATION\nB.Arch — CEPT University, Ahmedabad, 2024\nCOA Registration — Active\n\nINTERNSHIP\nArchitecture Intern — Vastu Shilpa, Ahmedabad (Jan 2024 – Jun 2024)\n • Prepared working drawings for residential projects in AutoCAD.\n • Created 3D visualizations using SketchUp and Lumion for client presentations.\n\nSKILLS\nAutoCAD, Revit, SketchUp, Lumion, Adobe Suite, building design, drafting`,
mid: `Kavya Bhatt — Project Architect\nAhmedabad | kavya.bhatt@email.com\n\nSUMMARY\nArchitect with 5 years in residential and institutional building design. All 10+ building plan submissions approved in first attempt.\n\nEXPERIENCE\nProject Architect — Vastu Shilpa, Ahmedabad (Jan 2021 – Present)\n • Designing township projects (200+ units) using AutoCAD and Revit.\n • All 10+ building plan submissions approved in first attempt.\n • Supervising construction of 50,000 sq.ft. institutional building.\n\nJunior Architect — HCP Design (Jul 2018 – Dec 2020)\n\nEDUCATION\nB.Arch — CEPT University, 2018\nCOA Registration — Active`,
senior: `Ar. Bijoy Jain — Principal Architect\nMumbai | bijoy.jain@email.com\n\nSUMMARY\nPrincipal Architect with 20 years leading an award-winning practice. Designed 50+ buildings across India. Won 10+ national architecture awards.\n\nEXPERIENCE\nPrincipal — Studio Mumbai (Jan 2005 – Present)\n • Leading a 30-person studio designing residential, institutional, and cultural projects.\n • Won RIBA International Prize, Aga Khan Award, and multiple IIA Gold Medals.\n • Projects published in 50+ international architecture journals.\n\nAssociate — Morphogenesis, Delhi (Jul 2000 – Dec 2004)\n\nEDUCATION\nM.Arch — Washington University, St. Louis, 2000`,
jd: `Architect — HCP Design, Ahmedabad\n\nRequirements:\n • B.Arch with COA registration\n • 4+ years design experience\n • AutoCAD and Revit proficiency\n • Building plan approval experience`
},

"Interior Design": {
entry: `Nikita Singh — Interior Design Trainee\nMumbai | nikita.singh@email.com\n\nSUMMARY\nInterior Design graduate with 3 portfolio projects including a cafe design and a 2BHK apartment renovation. Skilled in SketchUp and AutoCAD.\n\nEDUCATION\nBachelor of Interior Design — Rachana Sansad, Mumbai, 2024\n\nPROJECTS\n • Cafe Interior Concept: Complete interior design for a 1200 sq.ft cafe with mood boards, 3D renders, and material selection.\n • 2BHK Apartment Renovation: Space planning, furniture layout, and kitchen design.\n\nSKILLS\nAutoCAD, SketchUp, V-Ray, Photoshop, space planning, mood boards, material selection`,
mid: `Ritu Agarwal — Interior Designer\nMumbai | ritu.agarwal@email.com\n\nSUMMARY\nInterior designer with 4 years designing 40+ residential and commercial spaces. Budgets from INR 15L to 2Cr.\n\nEXPERIENCE\nSenior Designer — Livspace, Mumbai (Mar 2021 – Present)\n • Designing complete home interiors for 15-20 clients per year.\n • Managing project delivery with 90% on-time completion.\n • Coordinating with 10+ vendors for materials and installation.\n\nJunior Designer — Design Cafe, Bangalore (Jul 2019 – Feb 2021)\n\nSKILLS\nAutoCAD, SketchUp, V-Ray, space planning, furniture design, kitchen design, client management`,
senior: `Shabnam Gupta — Creative Director\nMumbai | shabnam.gupta@email.com\n\nSUMMARY\nCreative Director with 15 years in luxury interior design. Designed 200+ premium homes, hotels, and retail spaces. Featured in AD India, Elle Decor.\n\nEXPERIENCE\nCreative Director — The Orange Lane (Own Practice), Mumbai (Jan 2012 – Present)\n • Leading a 15-person studio designing luxury residential, hospitality, and retail interiors.\n • Designed interiors for 5 luxury hotels including Taj and Oberoi properties.\n • Featured in Architectural Digest India, Elle Decor, and GQ Living.\n\nSenior Designer — Sussanne Khan Design (Jul 2009 – Dec 2011)\n\nEDUCATION\nM.Des Interior Design — Parsons, New York, 2009`,
jd: `Interior Designer — Livspace, Bangalore\n\nRequirements:\n • 3+ years residential interior design\n • AutoCAD and SketchUp proficiency\n • Full project execution experience\n • Vendor management skills`
},

"Event Management": {
entry: `Tanvi Mehra — Event Coordinator Trainee\nDelhi | tanvi.mehra@email.com\n\nSUMMARY\nEvent management diploma holder with internship experience coordinating 10+ events including corporate meetups and product launches.\n\nEDUCATION\nDiploma in Event Management — NAEMD, Delhi, 2024\n\nINTERNSHIP\nEvent Intern — Wizcraft International, Delhi (Feb 2024 – May 2024)\n • Assisted in coordinating logistics for 10+ corporate events (50-200 attendees).\n • Managed guest registration desks and tracked RSVPs.\n\nSKILLS\nEvent coordination, vendor liaison, guest management, Excel, time management`,
mid: `Gaurav Malhotra — Event Manager\nDelhi | gaurav.m@email.com\n\nSUMMARY\nEvent manager with 5 years managing 100+ corporate events, weddings, and launches. Budgets up to INR 2Cr.\n\nEXPERIENCE\nSenior Event Manager — Wizcraft, Delhi (Apr 2021 – Present)\n • Managing 30+ events annually including conferences, launches, and award ceremonies.\n • Planned a 3-day tech conference for 2000+ attendees, 40 speakers, INR 1.5Cr budget.\n • Managing 50+ vendor relationships.\n\nEvent Coordinator — OML Entertainment (Jun 2018 – Mar 2021)\n\nSKILLS\nEvent planning, vendor management, budget management, production, client servicing`,
senior: `Rajeev Jain — CEO, Event Company\nMumbai | rajeev.jain@email.com\n\nSUMMARY\nCEO with 18 years building one of India's largest event management companies. Managed 500+ events including international summits with 10,000+ attendees.\n\nEXPERIENCE\nCEO — EventCraft (Own Company), Mumbai (Jan 2012 – Present)\n • Built a 100-person event company with INR 50Cr annual revenue.\n • Managed India's largest tech conference (10,000 attendees, 200 speakers).\n • Corporate client roster includes 20 Fortune 500 companies.\n\nSenior Event Producer — Wizcraft (Jul 2006 – Dec 2011)\n\nEDUCATION\nMBA — XLRI Jamshedpur, 2006`,
jd: `Event Manager — BookMyShow Live, Mumbai\n\nRequirements:\n • 4+ years event management\n • Large-scale event experience\n • Vendor management and budgeting\n • Strong organizational skills`
},

"Sports / Fitness": {
entry: `Karthik Reddy — Fitness Trainer (Fresher)\nBangalore | karthik.r@email.com\n\nSUMMARY\nB.P.Ed graduate with ACE personal trainer certification. Completed 3-month internship at a fitness center. Strong in exercise science and nutrition basics.\n\nEDUCATION\nB.P.Ed — Lakshmibai National Institute, Gwalior, 2024\n\nINTERNSHIP\nTrainer Intern — Gold's Gym, Bangalore (Mar 2024 – Jun 2024)\n • Conducted fitness assessments for 50+ new members.\n • Assisted in group fitness classes (HIIT, functional training).\n\nCERTIFICATIONS\nACE Personal Trainer, First Aid & CPR\n\nSKILLS\nExercise programming, fitness assessment, group coaching, nutrition basics, first aid`,
mid: `Rohan Kapoor — Fitness Trainer & S&C Coach\nBangalore | rohan.kapoor@email.com\n\nSUMMARY\nCertified trainer with 5 years, trained 500+ clients and 4 sports teams. Specialized in functional training and injury rehabilitation.\n\nEXPERIENCE\nHead Trainer — Cult.fit, Bangalore (Jun 2021 – Present)\n • Leading group classes for 50-80 daily participants.\n • Trained Bangalore FC reserve team, improving fitness scores by 18%.\n • Mentoring 8 junior trainers.\n\nTrainer — Gold's Gym, Mumbai (Jul 2018 – May 2021)\n\nCERTIFICATIONS\nACE Personal Trainer, NSCA-CSCS, First Aid & CPR`,
senior: `Ramji Srinivasan — Director of Sports Science\nBangalore | ramji.s@email.com\n\nSUMMARY\nDirector of Sports Science with 15 years working with Olympic athletes and IPL cricket teams. Published 10+ papers in sports science journals.\n\nEXPERIENCE\nDirector — JSW Sports, Bellary (Jun 2017 – Present)\n • Leading sports science department working with cricket, athletics, and football academies.\n • Designed periodization programs for 3 Olympic-level athletes.\n • Built a biomechanics lab with motion capture and force plate systems.\n\nHead S&C — Indian Cricket Team Support Staff (Jul 2012 – May 2017)\n\nEDUCATION\nPh.D. Sports Science — Loughborough University, UK, 2007`,
jd: `S&C Coach — JSW Sports\n\nRequirements:\n • 4+ years fitness training or conditioning\n • CSCS or ACE certification\n • Sports team experience\n • Knowledge of periodization and sports nutrition`
},

"Psychology / Counseling": {
entry: `Divya Iyer — Counseling Psychologist Trainee\nBangalore | divya.iyer@email.com\n\nSUMMARY\nM.A. Psychology graduate with RCI registration (provisional). Completed 300+ supervised counseling hours during M.Phil fieldwork. Trained in CBT basics.\n\nEDUCATION\nM.Phil Clinical Psychology — NIMHANS, 2024 (Ongoing)\nM.A. Psychology — Christ University, 2022\n\nCLINICAL HOURS\n • 300+ supervised counseling sessions covering anxiety, depression, and adjustment disorders.\n • Administered 50+ psychological assessments (BDI-II, BAI, WAIS-IV).\n\nSKILLS\nCBT basics, psychological assessment, counseling, case formulation, psychoeducation`,
mid: `Dr. Anjali Rao — Clinical Psychologist\nBangalore | dr.anjali.rao@email.com\n\nSUMMARY\nClinical psychologist with 5 years providing therapy for anxiety, depression, trauma. 3000+ sessions using CBT, DBT, and EMDR.\n\nEXPERIENCE\nClinical Psychologist — NIMHANS, Bangalore (Jun 2021 – Present)\n • Conducting 15-20 therapy sessions per week for GAD, MDD, PTSD, OCD.\n • Administering MMPI-2, BDI-II, BAI, WAIS-IV assessments.\n • Developed a 12-session CBT protocol for workplace anxiety.\n • Supervising 4 M.Phil trainees.\n\nCounselor — Fortis Mental Health (Aug 2018 – May 2021)\n\nEDUCATION\nM.Phil Clinical Psychology — NIMHANS, 2018\nRCI Registration — Active`,
senior: `Dr. Pratima Murthy — Professor & Head of Clinical Psychology\nBangalore | pratima.m@email.com\n\nSUMMARY\nProfessor with 22 years in clinical psychology. Guided 15 M.Phil and 5 Ph.D. students. Published 60+ papers. Advisor to WHO on mental health programs.\n\nEXPERIENCE\nProfessor & HOD — NIMHANS, Bangalore (Jun 2012 – Present)\n • Heading the clinical psychology department with 10 faculty and 30 trainees.\n • WHO consultant for District Mental Health Programme across 5 states.\n • Published 65 papers in journals including Lancet Psychiatry and BJP.\n\nAssociate Professor — NIMHANS (Jul 2005 – May 2012)\n\nEDUCATION\nPh.D. Clinical Psychology — NIMHANS, 2002\n\nPUBLICATIONS\n65 papers, h-index: 22, citations: 2400+`,
jd: `Clinical Psychologist — Manipal Hospital, Bangalore\n\nRequirements:\n • M.Phil Clinical Psychology with RCI registration\n • 3+ years clinical experience\n • CBT, DBT, or EMDR proficiency\n • Psychodiagnostic testing experience`
},

"Social Work": {
entry: `Aarti Kumari — Social Worker (Fresher)\nPune | aarti.kumari@email.com\n\nSUMMARY\nMSW graduate with fieldwork in child welfare and community development. Completed 200+ hours of supervised field placement in rural communities.\n\nEDUCATION\nMSW — TISS Mumbai, 2024\nB.A. Sociology — Pune University, 2022\n\nFIELD PLACEMENT\n • Community Development: Conducted 50+ household surveys and 10 community meetings on water sanitation in rural Pune.\n • Child Welfare: Assisted in child counseling and family visits for 20 cases at a children's home.\n\nSKILLS\nCommunity mobilization, case work, group work, participatory methods, report writing, Hindi/Marathi fluency`,
mid: `Fatima Sheikh — Program Manager\nPune | fatima.sheikh@email.com\n\nSUMMARY\nSocial worker with 6 years in community development, child welfare, and women's empowerment. Programs reaching 10,000+ beneficiaries.\n\nEXPERIENCE\nProgram Manager — Pratham Education, Pune (Mar 2021 – Present)\n • Managing remedial education across 50 government schools benefiting 8000+ children.\n • Supervising 25 field workers.\n • Preparing donor reports for 3 international funding agencies.\n\nSocial Worker — CORO India, Mumbai (Jun 2017 – Feb 2021)\n\nEDUCATION\nMSW — TISS Mumbai, 2017`,
senior: `Dr. Aruna Roy — Director, Social Development\nDelhi | aruna.roy@email.com\n\nSUMMARY\nDirector with 25 years in social development and policy advocacy. Led grassroots movements impacting 10M+ people. Awarded Magsaysay Award.\n\nEXPERIENCE\nDirector — MKSS (Mazdoor Kisan Shakti Sangathan), Rajasthan (Jan 2000 – Present)\n • Leading a grassroots organization that pioneered the Right to Information movement in India.\n • Influenced passage of MGNREGA, RTI Act, and Social Audit laws.\n • Trained 10,000+ community leaders across 10 states.\n\nSenior Advisor — UNDP India (Jul 2010 – Dec 2015)\n\nEDUCATION\nPh.D. Social Work — JNU, 1999`,
jd: `Program Manager — UNICEF India\n\nRequirements:\n • MSW or MA in Social Sciences\n • 5+ years in social development\n • Field team management experience\n • Proposal writing and donor reporting skills`
},

"Entrepreneurship / Startups": {
entry: `Arjun Sethi — Aspiring Entrepreneur / Product Intern\nBangalore | arjun.sethi@email.com\n\nSUMMARY\nB.Tech graduate who co-founded a college startup (food delivery on campus) serving 500+ students. Product development intern at a seed-stage startup.\n\nEDUCATION\nB.Tech CSE — NIT Surathkal, 2024\n\nSTARTUP EXPERIENCE\nCo-Founder — CampusBites (College Startup) (Aug 2022 – May 2024)\n • Built a campus food delivery platform using React Native serving 500+ students.\n • Generated INR 3L monthly revenue at peak. Managed a team of 5 delivery partners.\n\nINTERNSHIP\nProduct Intern — Razorpay, Bangalore (Jun 2023 – Aug 2023)\n • Assisted product team in user research and feature prioritization.\n\nSKILLS\nProduct thinking, React Native, user research, team building, pitching, basic financial modeling`,
mid: `Nikhil Agarwal — Startup Founder / Product Manager\nBangalore | nikhil.agarwal@email.com\n\nSUMMARY\nStartup founder and PM with 5 years building tech products. Co-founded an EdTech startup that grew to 50K users and INR 2Cr ARR before acquisition.\n\nEXPERIENCE\nProduct Manager — Chargebee, Chennai (Jun 2022 – Present)\n • Managing billing module used by 4000+ businesses.\n • Launched revenue recognition feature reducing manual effort by 60%.\n\nCo-Founder & CEO — LearnPath (EdTech), Bangalore (Jan 2019 – May 2022)\n • Built personalized learning platform, 0 to 50K users in 2 years.\n • Raised INR 1.5Cr seed funding. Team of 8. Acquired in 2022.\n\nEDUCATION\nB.Tech CSE — NIT Surathkal, 2018`,
senior: `Kunal Shah — Serial Entrepreneur / CEO\nMumbai | kunal.shah@email.com\n\nSUMMARY\nSerial entrepreneur with 15 years building and scaling companies. Founded 2 unicorn startups. Portfolio of 50+ angel investments. Regular speaker at global tech conferences.\n\nEXPERIENCE\nFounder & CEO — CRED, Bangalore (Apr 2018 – Present)\n • Built CRED from idea to $6.4B valuation with 20M+ users.\n • Raised $800M+ across 5 funding rounds from Tiger Global, Sequoia, DST.\n • Built a team of 800+ employees across product, engineering, and design.\n\nFounder — FreeCharge (Sep 2010 – Sep 2017)\n • Founded FreeCharge (acquired by Snapdeal for $450M in 2015).\n • Grew to 50M+ registered users and $1B+ annual transaction volume.\n\nEDUCATION\nMBA — Narsee Monjee, Mumbai, 2004`,
jd: `Product Manager — Razorpay, Bangalore\n\nRequirements:\n • 3+ years product management in tech/SaaS\n • Experience taking products from concept to launch\n • Strong analytical skills with product analytics tools\n • Startup or founding experience preferred`
},

"Pharmacy": {
entry: `Sneha Pillai — Hospital Pharmacist (Fresher)\nChennai | sneha.pillai@email.com\n\nSUMMARY\nPharm.D. graduate with 6 months of clinical rotations in hospital pharmacy. Trained in prescription review, drug dispensing, and patient counseling.\n\nEDUCATION\nPharm.D. — JSS College of Pharmacy, Ooty, 2024\n\nCLINICAL ROTATIONS\n • Reviewed 50+ prescriptions daily for drug interactions and dosing.\n • Counseled 20+ patients on medication usage and side effects.\n • Assisted in IV admixture preparation under supervision.\n\nREGISTRATIONS\nTN Pharmacy Council — Provisional Registration\n\nSKILLS\nPrescription review, drug dispensing, patient counseling, pharmacovigilance basics, pharmacy informatics`,
mid: `Deepa Ramesh — Clinical Pharmacist\nChennai | deepa.ramesh@email.com\n\nSUMMARY\nClinical pharmacist with 4 years in hospital pharmacy. Reviewed 15,000+ prescriptions. Active in antibiotic stewardship committee.\n\nEXPERIENCE\nClinical Pharmacist — Apollo Hospitals, Chennai (Aug 2021 – Present)\n • Reviewing 100+ prescriptions daily for drug interactions and contradictions.\n • Active member of Antibiotic Stewardship Committee.\n • Counseling 30+ patients daily on medications.\n\nHospital Pharmacist — Kauvery Hospital (Jul 2019 – Jul 2021)\n\nEDUCATION\nPharm.D. — JSS College of Pharmacy, 2019\n\nREGISTRATIONS\nTN Pharmacy Council — Active`,
senior: `Dr. Ramesh Kumar — Director of Pharmacy Services\nMumbai | ramesh.kumar@email.com\n\nSUMMARY\nDirector of Pharmacy with 16 years managing hospital pharmacy operations for multi-specialty and super-specialty hospitals. Led NABH accreditation for pharmacy services.\n\nEXPERIENCE\nDirector Pharmacy — Kokilaben Hospital, Mumbai (Jun 2017 – Present)\n • Overseeing pharmacy operations for a 750-bed super-specialty hospital with 50+ pharmacy staff.\n • Implemented unit-dose dispensing system reducing medication errors by 60%.\n • Led pharmacy automation with robotic dispensing for high-volume medications.\n\nChief Pharmacist — Fortis Healthcare, Delhi (Jul 2011 – May 2017)\n\nEDUCATION\nPh.D. Pharmacy Practice — BITS Pilani, 2011`,
jd: `Clinical Pharmacist — Max Healthcare, Delhi\n\nRequirements:\n • Pharm.D. or M.Pharm with pharmacy council registration\n • 3+ years hospital pharmacy experience\n • Prescription review and drug interaction screening\n • Patient counseling skills`
},

};

// ── Domain List for Dropdown ──────────────────────────────────────────────────
const DOMAIN_LIST = Object.keys(SAMPLE_DATA);
