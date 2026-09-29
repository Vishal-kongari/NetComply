import React, { useState } from "react";

import {
    ShieldCheck,
    Upload,
    FileText,
    Server,
    Brain,
    Database,
    Blocks,
    CheckCircle,
    XCircle,
    AlertTriangle,
    RefreshCw
} from "lucide-react";

function App() {

    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");

    const handleFileChange = (e) => {

        const selectedFile = e.target.files[0];

        if (!selectedFile) return;

        setFile(selectedFile);
        setResult(null);
        setError("");
    };


    const analyzeConfiguration = async () => {

        if (!file) {
            setError("Please select a configuration file.");
            return;
        }

        setLoading(true);
        setError("");

        const formData = new FormData();

        formData.append("file", file);

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/analyze",
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok) {
                throw new Error("Backend request failed");
            }

            const data = await response.json();

            setResult(data);

        } catch (err) {

            setError(
                "Unable to connect to FastAPI backend. Make sure the backend is running."
            );

        } finally {

            setLoading(false);

        }
    };


    const getStatistics = () => {

        if (!result?.compliance) {
            return {
                pass: 0,
                fail: 0,
                total: 0
            };
        }

        const pass =
            result.compliance.filter(
                item => item.status === "PASS"
            ).length;

        const fail =
            result.compliance.filter(
                item => item.status === "FAIL"
            ).length;

        return {
            pass,
            fail,
            total: result.compliance.length
        };
    };


    const stats = getStatistics();


    return (

        <div className="app">

            {/* SIDEBAR */}

            <aside className="sidebar">

                <div className="brand">

                    <div className="brand-icon">
                        <ShieldCheck size={25} />
                    </div>

                    <div>
                        <h2>NetSecure</h2>
                        <span>Compliance Engine</span>
                    </div>

                </div>


                <nav>

                    <div className="nav-item active">
                        <Server size={19} />
                        Dashboard
                    </div>

                    <div className="nav-item">
                        <FileText size={19} />
                        Configurations
                    </div>

                    <div className="nav-item">
                        <ShieldCheck size={19} />
                        Compliance
                    </div>

                    <div className="nav-item">
                        <Brain size={19} />
                        AI Assistant
                    </div>

                    <div className="nav-item">
                        <Blocks size={19} />
                        Audit History
                    </div>

                </nav>


                <div className="sidebar-bottom">

                    <span>AI + Cybersecurity</span>
                    <span>+ Blockchain</span>

                </div>

            </aside>


            {/* MAIN */}

            <main className="main">

                <header className="header">

                    <div>

                        <p className="eyebrow">
                            SECURITY OPERATIONS
                        </p>

                        <h1>
                            Network Compliance Dashboard
                        </h1>

                        <p className="subtitle">
                            Vendor-agnostic configuration analysis
                            and security compliance.
                        </p>

                    </div>

                    <div className="system-status">

                        <span className="status-dot"></span>

                        System Online

                    </div>

                </header>


                {/* UPLOAD */}

                <section className="upload-card">

                    <div className="upload-info">

                        <div className="section-icon">
                            <Upload size={23} />
                        </div>

                        <div>

                            <h3>
                                Analyze Network Configuration
                            </h3>

                            <p>
                                Upload a Cisco, Juniper, Fortinet,
                                Palo Alto or other configuration file.
                            </p>

                        </div>

                    </div>


                    <div className="upload-controls">

                        <label className="file-input">

                            <input
                                type="file"
                                accept=".cfg,.txt,.xml,.json"
                                onChange={handleFileChange}
                            />

                            <FileText size={18} />

                            {file
                                ? file.name
                                : "Choose configuration"}

                        </label>


                        <button
                            className="analyze-button"
                            onClick={analyzeConfiguration}
                            disabled={loading}
                        >

                            {loading ? (

                                <>
                                    <RefreshCw
                                        size={18}
                                        className="spin"
                                    />

                                    Analyzing...

                                </>

                            ) : (

                                <>
                                    <ShieldCheck size={18} />
                                    Analyze
                                </>

                            )}

                        </button>

                    </div>


                    {error && (

                        <div className="error-message">
                            <AlertTriangle size={17} />
                            {error}
                        </div>

                    )}

                </section>


                {/* STATISTICS */}

                <section className="stats">

                    <StatCard
                        title="Total Checks"
                        value={stats.total}
                        icon={<ShieldCheck />}
                    />

                    <StatCard
                        title="Passed"
                        value={stats.pass}
                        icon={<CheckCircle />}
                        type="success"
                    />

                    <StatCard
                        title="Failed"
                        value={stats.fail}
                        icon={<XCircle />}
                        type="danger"
                    />

                    <StatCard
                        title="Vendor"
                        value={result?.vendor || "--"}
                        icon={<Server />}
                    />

                </section>


                {/* RESULTS */}

                {result ? (

                    <>

                        <section className="grid">

                            {/* NORMALIZED CONFIG */}

                            <div className="panel">

                                <div className="panel-header">

                                    <div>

                                        <h3>
                                            Normalized Configuration
                                        </h3>

                                        <p>
                                            Common security model
                                        </p>

                                    </div>

                                    <Database size={20} />

                                </div>


                                <pre className="json-view">

                                    {JSON.stringify(
                                        result.normalized_configuration,
                                        null,
                                        2
                                    )}

                                </pre>

                            </div>


                            {/* BLOCKCHAIN */}

                            <div className="panel blockchain">

                                <div className="panel-header">

                                    <div>

                                        <h3>
                                            Blockchain Audit
                                        </h3>

                                        <p>
                                            Tamper-evident record
                                        </p>

                                    </div>

                                    <Blocks size={20} />

                                </div>


                                <div className="hash-box">

                                    <span>
                                        SHA-256 Hash
                                    </span>

                                    <code>
                                        {result.blockchain?.hash}
                                    </code>

                                </div>


                                <div className="blockchain-status">

                                    <CheckCircle size={18} />

                                    Audit record generated

                                </div>

                            </div>

                        </section>


                        {/* COMPLIANCE TABLE */}

                        <section className="panel">

                            <div className="panel-header">

                                <div>

                                    <h3>
                                        Compliance Findings
                                    </h3>

                                    <p>
                                        Security framework evaluation
                                    </p>

                                </div>

                                <ShieldCheck size={20} />

                            </div>


                            <div className="table-container">

                                <table>

                                    <thead>

                                        <tr>

                                            <th>Rule</th>
                                            <th>Status</th>
                                            <th>Severity</th>
                                            <th>Evidence</th>
                                            <th>Remediation</th>

                                        </tr>

                                    </thead>


                                    <tbody>

                                        {result.compliance?.map(
                                            (item, index) => (

                                                <tr key={index}>

                                                    <td>
                                                        <strong>
                                                            {item.rule}
                                                        </strong>
                                                    </td>

                                                    <td>

                                                        {item.status === "PASS" ? (

                                                            <span className="badge pass">
                                                                <CheckCircle size={14} />
                                                                PASS
                                                            </span>

                                                        ) : (

                                                            <span className="badge fail">
                                                                <XCircle size={14} />
                                                                FAIL
                                                            </span>

                                                        )}

                                                    </td>

                                                    <td>

                                                        <span
                                                            className={
                                                                "severity " +
                                                                item.severity.toLowerCase()
                                                            }
                                                        >
                                                            {item.severity}
                                                        </span>

                                                    </td>

                                                    <td>
                                                        {item.evidence}
                                                    </td>

                                                    <td>
                                                        {item.remediation}
                                                    </td>

                                                </tr>

                                            )
                                        )}

                                    </tbody>

                                </table>

                            </div>

                        </section>


                        {/* UNKNOWN COMMANDS */}

                        <section className="panel">

                            <div className="panel-header">

                                <div>

                                    <h3>
                                        AI / Unknown Commands
                                    </h3>

                                    <p>
                                        Commands requiring AI interpretation
                                    </p>

                                </div>

                                <Brain size={20} />

                            </div>


                            {result.unknown_commands?.length > 0 ? (

                                <div className="commands">

                                    {result.unknown_commands.map(
                                        (command, index) => (

                                            <div
                                                className="command"
                                                key={index}
                                            >

                                                <span>
                                                    {command}
                                                </span>

                                                <span className="ai-tag">
                                                    AI Review
                                                </span>

                                            </div>

                                        )
                                    )}

                                </div>

                            ) : (

                                <div className="empty">
                                    No unknown commands detected.
                                </div>

                            )}

                        </section>

                    </>

                ) : (

                    <section className="empty-state">

                        <div className="empty-icon">
                            <ShieldCheck size={42} />
                        </div>

                        <h2>
                            Ready for Configuration Analysis
                        </h2>

                        <p>
                            Upload a network configuration file
                            to begin compliance analysis.
                        </p>

                    </section>

                )}

            </main>

        </div>

    );
}


/* STAT CARD */

function StatCard({
    title,
    value,
    icon,
    type = ""
}) {

    return (

        <div className={"stat-card " + type}>

            <div className="stat-icon">
                {icon}
            </div>

            <div>

                <span>
                    {title}
                </span>

                <strong>
                    {value}
                </strong>

            </div>

        </div>

    );

}


export default App;