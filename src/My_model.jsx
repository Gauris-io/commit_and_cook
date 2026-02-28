import React, { useEffect } from 'react'
import { useGLTF, useAnimations } from '@react-three/drei'

export default function Model(props) {
  // Path points to your public folder
  const { scene, animations } = useGLTF('/glbfile.glb')
  const { actions } = useAnimations(animations, scene)

  useEffect(() => {
    // Check console (F12) if it doesn't spin
    console.log("Animations found:", Object.keys(actions))
    
    if (actions && Object.keys(actions).length > 0) {
      // Plays the first animation found in the file
      const firstAction = Object.values(actions)[0]
      firstAction.play()
    }
  }, [actions])

  return <primitive object={scene} {...props} />
}

useGLTF.preload('/glbfile.glb')