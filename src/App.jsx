import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stage, Environment } from '@react-three/drei'
import { Suspense } from 'react'
import Model from './My_model'

export default function App() {
  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh', background: '#050505', color: 'white' }}>
      
      {/* Left side for Project Information */}
      <div style={{ flex: 2, padding: '50px', fontFamily: 'sans-serif', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <h1 style={{ color: '#ff4d4d', fontSize: '3rem', margin: 0 }}>Commit & Cook</h1>
        <p style={{ fontSize: '1.2rem', opacity: 0.8 }}>Molecular Flavor Explorer</p>
        <div style={{ marginTop: '30px', borderLeft: '2px solid #ff4d4d', paddingLeft: '20px' }}>
          <h3>Active Profile: Roasted</h3>
          <p>Analyzing: 2-Propylpyrazine</p>
        </div>
      </div>

      {/* Right side for 3D Earth (3rd-4th part of screen) */}
      <div style={{ flex: 1 }}>
        <Canvas shadows camera={{ position: [0, 0, 5], fov: 45 }}>
          <Suspense fallback={null}>
            <Stage environment="city" intensity={0.5} adjustCamera>
              <Model />
            </Stage>
          </Suspense>
          <OrbitControls makeDefault enablePan={false} />
        </Canvas>
      </div>

    </div>
  )
}