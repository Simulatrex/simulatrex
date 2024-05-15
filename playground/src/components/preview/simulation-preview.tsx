import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Plane, Sphere } from "@react-three/drei";

type Agent = {
  id: string;
};

type PreviewProps = {
  agents: Agent[];
};

const Preview: React.FC<PreviewProps> = ({ agents }) => {
  // Calculate the size of the environment based on the agents' positions
  const size = 20; // Example size, this can be dynamic
  const tileColor = "#EEF0F4"; // Light grey for the tiles
  const [hoveredAgentId, setHoveredAgentId] = useState<string | null>(null);
  console.log(agents);

  return (
    <Canvas camera={{ position: [size / 2, size, size * 2], fov: 60 }}>
      <ambientLight intensity={0.8} />
      <pointLight position={[size, size, size]} castShadow />

      <OrbitControls enableRotate={false} />

      {/* Create a tilted plane to represent the environment */}
      <Plane
        rotation={[-Math.PI / 2, 0, 0]} // rotate the plane to be horizontal
        position={[size / 2 - 5, 0, size / 2]}
        args={[size, size]} // size of the plane
      >
        <meshStandardMaterial attach="material" color={tileColor} />
      </Plane>

      {/* Positioning agents on the plane */}

      {agents &&
        agents.length > 0 &&
        agents.map((agent, index) => {
          // Distribute agents evenly across the plane
          const xPosition =
            (index % Math.ceil(Math.sqrt(agents.length))) *
            (size / Math.ceil(Math.sqrt(agents.length)));
          const zPosition =
            Math.floor(index / Math.ceil(Math.sqrt(agents.length))) *
            (size / Math.ceil(Math.sqrt(agents.length)));

          // Increase yPosition to lift agents further above the plane
          const yPosition = 0.5; // Adjust this value as needed to lift agents higher

          // Calculate new positions with margin, keeping xPosition and zPosition calculations the same
          const newPosition: [number, number, number] = [
            xPosition,
            yPosition,
            zPosition,
          ];

          const agentSize = size / 10; // Adjust size as needed

          return (
            <React.Fragment key={agent.id}>
              <Sphere
                castShadow
                receiveShadow
                position={newPosition}
                args={[agentSize, 32, 32]}
                rotation={[0, Math.random() * Math.PI * 2, 0]}
                onClick={() => {
                  setHoveredAgentId(agent.id);
                }}
              >
                <meshStandardMaterial attach="material" color="red" />
              </Sphere>
            </React.Fragment>
          );
        })}
    </Canvas>
  );
};

export default Preview;
