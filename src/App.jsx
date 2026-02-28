import { Canvas } from '@react-three/fiber'
import { Stage, Html, useProgress } from '@react-three/drei'
import { Suspense } from 'react'
import Model from './My_model'
import './App.css'

function Loader() {
  const { progress } = useProgress()
  return <Html center><div className="loading-txt">{progress.toFixed(0)}%</div></Html>
}

export default function App() {
  // We create 54 tiles (3 sets of 18) to ensure full screen coverage
  const flavorImages = Array.from({ length: 54 }, (_, i) => ({
    id: i,
    num: (i % 18) + 1,
    // Random rotation between -20 and 20 degrees for a 'messy' tile look
    rotation: Math.floor(Math.random() * 40) - 20 
  }));

  return (
    <div className="main-scenic-wrapper">
      <div className="scenic-bg illustrated-hills"></div>
      
      {/* Tiled Background Layer */}
      <div className="tile-grid-container">
        {flavorImages.map((img) => (
          <div key={img.id} className="tile-cell">
            <img 
              src={`/images/f${img.num}.png`} 
              className="tile-img" 
              style={{ transform: `rotate(${img.rotation}deg)` }}
              alt="" 
            />
          </div>
        ))}
      </div>

      {/* Central Earth Focus */}
      <div className="hero-container">
        <h1 className="main-title">crave-it!</h1>
        <div className="earth-wrapper" style={{ pointerEvents: 'none' }}>
          <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
            <Suspense fallback={<Loader />}>
              <Stage environment="city" intensity={0.7} shadows={false}>
                <Model scale={1.2} /> 
              </Stage>
            </Suspense>
          </Canvas>
        </div>
      </div>
    </div>
  )
}