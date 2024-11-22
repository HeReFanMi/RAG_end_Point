<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAG System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }
        header {
            background-color: #333;
            color: white;
            padding: 20px;
            text-align: center;
        }
        h1, h2 {
            margin: 0 0 10px 0;
        }
        h3 {
            margin: 20px 0 10px 0;
        }
        section {
            padding: 20px;
            margin: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        pre {
            background-color: #2c3e50;
            color: white;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        code {
            background-color: #ecf0f1;
            padding: 2px 5px;
            border-radius: 3px;
        }
        ul {
            list-style-type: none;
            padding-left: 0;
        }
        li {
            margin: 5px 0;
        }
        .steps {
            margin-left: 20px;
        }
        .api-response {
            margin-top: 10px;
        }
        .environment-variables {
            background-color: #ecf0f1;
            padding: 10px;
            border-radius: 5px;
        }
        footer {
            text-align: center;
            padding: 10px;
            background-color: #333;
            color: white;
        }
    </style>
</head>
<body>

<header>
    <h1>RAG System</h1>
</header>

<section>
    <h2>Overview</h2>
    <p>The RAG (Retrieval-Augmented Generation) system is a core component of the HereFamni project. It integrates retrieval and generation capabilities to address the detection of healthcare-related fake news. By leveraging a database of vector embeddings, the RAG model retrieves relevant content and generates responses augmented by this information.</p>
</section>

<section>
    <h2>Features</h2>
    <ul>
        <li>Retrieves context-relevant information from a knowledge base.</li>
        <li>Generates responses enriched with retrieved information.</li>
        <li>Exposes API endpoints for integration with external systems.</li>
    </ul>
</section>

<section>
    <h2>Setup Instructions</h2>
    <h3>Prerequisites</h3>
    <ul>
        <li>Docker and Docker Compose installed.</li>
        <li>A running PostgreSQL database container (configured separately).</li>
    </ul>

    <h3>Steps</h3>
    <ol class="steps">
        <li>Clone the repository:
            <pre><code>git clone https://github.com/HeReFanMi/Rag.git
cd Rag</code></pre>
        </li>
        <li>Build and Run the Docker Container:
            <pre><code>docker build -t ragystem-flask-app .
docker-compose up</code></pre>
        </li>
        <li>Access the Application: Once the containers are running, access the API at:
            <pre><code>http://localhost:5000</code></pre>
        </li>
    </ol>
</section>

<section>
    <h2>API Endpoints</h2>
    <h3>POST /find_similar_chunks</h3>
    <p><strong>Description:</strong> Retrieve similar content chunks from the knowledge base.</p>
    <p><strong>Request Body:</strong></p>
    <pre><code>{
  "query": "Your query string here"
}</code></pre>
    <p><strong>Response:</strong></p>
    <pre><code>{
  "results": [
    {"chunk_id": 1, "content": "Sample content", "score": 0.9},
    ...
  ]
}</code></pre>
</section>

<section>
    <h2>Environment Variables</h2>
    <div class="environment-variables">
        <p>The following environment variables are used to configure the system:</p>
        <ul>
            <li><strong>DB_HOST</strong>: Hostname or IP address of the database.</li>
            <li><strong>DB_PORT</strong>: Port number for the database (default: <code>5432</code>).</li>
            <li><strong>DB_USER</strong>: Username for database access.</li>
            <li><strong>DB_PASSWORD</strong>: Password for database access.</li>
            <li><strong>DB_NAME</strong>: Database name.</li>
        </ul>
    </div>
</section>

<section>
    <h2>Network Configuration</h2>
    <p>Ensure that the <code>ragystem_shared-network</code> Docker network is used for communication between containers. Verify it using:</p>
    <pre><code>docker network inspect ragystem_shared-network</code></pre>
</section>

<section>
    <h2>Contributing</h2>
    <ol class="steps">
        <li>Fork the repository.</li>
        <li>Create a feature branch.</li>
        <li>Commit your changes and open a pull request.</li>
    </ol>
</section>

<footer>
    <p>This project is licensed under the MIT License.</p>
</footer>

</body>
</html>
