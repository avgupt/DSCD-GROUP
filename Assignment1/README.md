# Protobuf Compile:
<pre><code>
    protoc -I=. --python_out=. grpc/server/server.proto
</code></pre>

# gRPC Compile:
<pre><code>
    python -m grpc_tools.protoc -I=. --python_out=. --pyi_out=. --grpc_python_out=.  grpc/server/server.proto
</code></pre>
