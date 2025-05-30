INSERT INTO users (email, fullname, is_active, salt, hashed_password)
VALUES ('master@user.com', 'MasterUser', true, 'qwerty', 'password')
RETURNING id;



-- Вставка 100 организаций для owner_id = 1
INSERT INTO organizations (owner_id, title)
VALUES (1, 'Alpha Innovations'),
       (1, 'Beta Solutions'),
       (1, 'Gamma Enterprises'),
       (1, 'Delta Dynamics'),
       (1, 'Epsilon Labs'),
       (1, 'Zeta Tech'),
       (1, 'Eta Analytics'),
       (1, 'Theta Software'),
       (1, 'Iota Group'),
       (1, 'Kappa Systems'),
       (1, 'Lambda Network'),
       (1, 'Mu Media'),
       (1, 'Nu Nexus'),
       (1, 'Xi Cloud'),
       (1, 'Omicron AI'),
       (1, 'Pi Robotics'),
       (1, 'Rho Innovations'),
       (1, 'Sigma Corp'),
       (1, 'Tau Logistics'),
       (1, 'Upsilon Fintech'),
       (1, 'Phi Consulting'),
       (1, 'Chi Ventures'),
       (1, 'Psi Health'),
       (1, 'Omega Cybersecurity'),
       (1, 'Nova Labs'),
       (1, 'Quantum Dynamics'),
       (1, 'Neural Bridge'),
       (1, 'Synth AI'),
       (1, 'MindMesh'),
       (1, 'VisionFlow'),
       (1, 'HyperStack'),
       (1, 'CoreData Inc.'),
       (1, 'DeepStream'),
       (1, 'BrightWorks'),
       (1, 'EchoTech'),
       (1, 'PulseSoft'),
       (1, 'Skyline Solutions'),
       (1, 'IntelliSpace'),
       (1, 'CloudForge'),
       (1, 'Zenith Ventures'),
       (1, 'MetaCore'),
       (1, 'InsightIQ'),
       (1, 'SecureShift'),
       (1, 'Pathway Systems'),
       (1, 'Streamline IT'),
       (1, 'TrueNorth Innovations'),
       (1, 'NextPhase AI'),
       (1, 'AxonEdge'),
       (1, 'ClarityCloud'),
       (1, 'BridgeLogic'),
       (1, 'NeoLabs'),
       (1, 'Vector AI'),
       (1, 'Orbit Enterprises'),
       (1, 'Cascade Systems'),
       (1, 'Everbyte'),
       (1, 'NimbusTech'),
       (1, 'CortexAI'),
       (1, 'Digital Frontier'),
       (1, 'Skyport Global'),
       (1, 'Aurora Analytics'),
       (1, 'BlueNova'),
       (1, 'Helix Labs'),
       (1, 'Quantum Leap'),
       (1, 'Infinity Systems'),
       (1, 'Artemis Solutions'),
       (1, 'ByteWorks'),
       (1, 'Horizon Dynamics'),
       (1, 'Vertex Systems'),
       (1, 'CoreShift'),
       (1, 'LumenTech'),
       (1, 'FusionLogix'),
       (1, 'Elevate Labs'),
       (1, 'Nucleus Cloud'),
       (1, 'Solstice AI'),
       (1, 'Nebula Innovations'),
       (1, 'Triad Group'),
       (1, 'VortexIQ'),
       (1, 'Aether Technologies'),
       (1, 'PulseGrid'),
       (1, 'NimbleSoft'),
       (1, 'BrightPath'),
       (1, 'Altura AI'),
       (1, 'Pinnacle Systems'),
       (1, 'DataCurrent'),
       (1, 'SparkLogic'),
       (1, 'CodeCrux'),
       (1, 'Ignite Labs'),
       (1, 'PrismShift'),
       (1, 'AstroEdge'),
       (1, 'EcoStream'),
       (1, 'Skychain'),
       (1, 'Glide Solutions'),
       (1, 'NovaLink'),
       (1, 'ShiftSpace'),
       (1, 'Adaptix AI'),
       (1, 'Intuition Tech'),
       (1, 'EchoMind'),
       (1, 'SynapseCore'),
       (1, 'OrbitMind'),
       (1, 'DigitalEcho'),
       (1, 'SignalStack'),
       (1, 'Scalability Inc.'),
       (1, 'LucidMetrics'),
       (1, 'NeuroScale');
