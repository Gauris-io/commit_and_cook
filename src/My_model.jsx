import React, { useRef } from 'react'
import { useGLTF } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'

export default function Model(props) {
  const group = useRef()
  // Ensure glbfile.glb is in your public/ folder
  const { scene } = useGLTF('/glbfile.glb')

  // Infinite, non-interactive code-based rotation
  useFrame((state, delta) => {
    if (group.current) {
      group.current.rotation.y += delta * 0.12 
    }
  })

  return <primitive ref={group} object={scene} {...props} />
}

useGLTF.preload('/glbfile.glb')