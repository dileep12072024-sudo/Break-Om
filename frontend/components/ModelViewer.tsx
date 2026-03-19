'use client'

import { Suspense, useRef, useState, useEffect } from 'react'
import { Canvas, useFrame, useLoader } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, Environment, Grid, Stats } from '@react-three/drei'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader'
import * as THREE from 'three'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Separator } from '@/components/ui/separator'
import { 
  Download, 
  RotateCcw, 
  ZoomIn, 
  ZoomOut, 
  Maximize2, 
  Grid3x3,
  Sun,
  Move,
  Edit3,
  Loader2,
  Box
} from 'lucide-react'
import { toast } from 'sonner'
import axios from 'axios'

interface ModelViewerProps {
  modelId: string | null
}

function Model({ url, format }: { url: string; format: string }) {
  const meshRef = useRef<THREE.Group>(null)
  const [model, setModel] = useState<THREE.Group | null>(null)

  useEffect(() => {
    if (!url) return

    const loadModel = async () => {
      try {
        let loader
        switch (format) {
          case 'glb':
          case 'gltf':
            loader = new GLTFLoader()
            break
          case 'obj':
            loader = new OBJLoader()
            break
          case 'fbx':
            loader = new FBXLoader()
            break
          default:
            loader = new GLTFLoader()
        }

        loader.load(
          url,
          (loadedModel) => {
            const group = format === 'glb' || format === 'gltf' 
              ? (loadedModel as any).scene 
              : loadedModel as THREE.Group

            // Center and scale the model
            const box = new THREE.Box3().setFromObject(group)
            const center = box.getCenter(new THREE.Vector3())
            const size = box.getSize(new THREE.Vector3())
            
            const maxDim = Math.max(size.x, size.y, size.z)
            const scale = 2 / maxDim
            
            group.scale.setScalar(scale)
            group.position.sub(center.multiplyScalar(scale))
            
            setModel(group)
          },
          (progress) => {
            console.log('Loading progress:', (progress.loaded / progress.total) * 100 + '%')
          },
          (error) => {
            console.error('Error loading model:', error)
          }
        )
      } catch (error) {
        console.error('Failed to load model:', error)
      }
    }

    loadModel()
  }, [url, format])

  useFrame((state, delta) => {
    if (meshRef.current && model) {
      // Gentle rotation animation
      meshRef.current.rotation.y += delta * 0.2
    }
  })

  if (!model) {
    return (
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="#666" wireframe />
      </mesh>
    )
  }

  return (
    <group ref={meshRef}>
      <primitive object={model} />
    </group>
  )
}

function Scene({ modelId, format }: { modelId: string; format: string }) {
  return (
    <>
      <PerspectiveCamera makeDefault position={[5, 5, 5]} />
      <OrbitControls 
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={1}
        maxDistance={20}
      />
      <Environment preset="sunset" background={false} />
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <directionalLight position={[-10, -10, -5]} intensity={0.5} />
      
      <Grid 
        args={[20, 20]} 
        cellSize={1} 
        cellThickness={0.5} 
        cellColor="#6b7280" 
        sectionSize={5} 
        sectionThickness={1} 
        sectionColor="#374151" 
        fadeDistance={30} 
        fadeStrength={1} 
        followCamera={false} 
      />
      
      <Model url={`${process.env.NEXT_PUBLIC_API_URL}/api/v1/models/${modelId}/download?format=${format}`} format={format} />
    </>
  )
}

export function ModelViewer({ modelId }: ModelViewerProps) {
  const [format, setFormat] = useState('obj')
  const [isEditing, setIsEditing] = useState(false)
  const [editPrompt, setEditPrompt] = useState('')
  const [isDownloading, setIsDownloading] = useState(false)
  const [showGrid, setShowGrid] = useState(true)
  const [autoRotate, setAutoRotate] = useState(true)
  const [modelInfo, setModelInfo] = useState<any>(null)

  useEffect(() => {
    if (modelId) {
      fetchModelInfo()
    }
  }, [modelId])

  const fetchModelInfo = async () => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/models/${modelId}`)
      setModelInfo(response.data)
      if (response.data?.format) {
        setFormat(response.data.format)
      }
    } catch (error) {
      console.error('Failed to fetch model info:', error)
    }
  }

  const handleEdit = async () => {
    if (!editPrompt.trim()) {
      toast.error('Please enter an edit prompt')
      return
    }

    setIsEditing(true)
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/models/edit`,
        {
          model_id: modelId,
          edit_prompt: editPrompt,
          format: format
        }
      )

      if (response.data.success) {
        toast.success('Model edited successfully!')
        setEditPrompt('')
        fetchModelInfo() // Refresh model info
      } else {
        toast.error(response.data.message || 'Edit failed')
      }
    } catch (error: any) {
      console.error('Edit error:', error)
      toast.error(
        error.response?.data?.detail || 
        error.message || 
        'Failed to edit model'
      )
    } finally {
      setIsEditing(false)
    }
  }

  const handleDownload = async () => {
    setIsDownloading(true)
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/models/${modelId}/download?format=${format}`,
        {
          responseType: 'blob'
        }
      )

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${modelId}.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)

      toast.success('Model downloaded successfully!')
    } catch (error: any) {
      console.error('Download error:', error)
      toast.error('Failed to download model')
    } finally {
      setIsDownloading(false)
    }
  }

  const resetCamera = () => {
    // This would reset the camera position
    window.location.reload()
  }

  if (!modelId) {
    return (
      <Card className="h-full">
        <CardContent className="flex items-center justify-center h-full">
          <div className="text-center space-y-4">
            <Box className="h-16 w-16 mx-auto text-muted-foreground" />
            <div>
              <h3 className="text-lg font-semibold">No Model Selected</h3>
              <p className="text-sm text-muted-foreground">
                Generate or select a model to view it here
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="h-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Box className="h-5 w-5" />
            3D Model Viewer
          </CardTitle>
          <div className="flex items-center gap-2">
            <Badge variant="secondary">
              {format.toUpperCase()}
            </Badge>
            {modelInfo && (
              <Badge variant="outline">
                {(modelInfo.file_size / 1024 / 1024).toFixed(2)} MB
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* 3D Viewer */}
        <div className="h-[400px] rounded-lg overflow-hidden border">
          <Canvas shadows camera={{ position: [5, 5, 5], fov: 50 }}>
            <Suspense fallback={null}>
              <Scene modelId={modelId} format={format} />
            </Suspense>
          </Canvas>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-2 flex-wrap">
          <Button
            variant="outline"
            size="sm"
            onClick={resetCamera}
          >
            <RotateCcw className="h-4 w-4 mr-2" />
            Reset View
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowGrid(!showGrid)}
          >
            <Grid3x3 className="h-4 w-4 mr-2" />
            Grid
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => setAutoRotate(!autoRotate)}
          >
            <Move className="h-4 w-4 mr-2" />
            Auto Rotate
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={handleDownload}
            disabled={isDownloading}
          >
            {isDownloading ? (
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            ) : (
              <Download className="h-4 w-4 mr-2" />
            )}
            Download
          </Button>
        </div>

        <Separator />

        {/* AI Editing */}
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Edit3 className="h-4 w-4" />
            <h4 className="text-sm font-semibold">AI Editing</h4>
          </div>
          
          <div className="flex gap-2">
            <Input
              placeholder="e.g., make the wings longer, change texture to metallic..."
              value={editPrompt}
              onChange={(e) => setEditPrompt(e.target.value)}
              className="flex-1"
            />
            <Button
              onClick={handleEdit}
              disabled={isEditing || !editPrompt.trim()}
              size="sm"
            >
              {isEditing ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                'Edit'
              )}
            </Button>
          </div>
        </div>

        <Separator />

        {/* Format Selection */}
        <div className="space-y-2">
          <label className="text-sm font-medium">Export Format</label>
          <div className="flex gap-2">
            {(['glb', 'obj', 'fbx'] as const).map((fmt) => (
              <Button
                key={fmt}
                variant={format === fmt ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFormat(fmt)}
              >
                {fmt.toUpperCase()}
              </Button>
            ))}
          </div>
        </div>

        {/* Model Info */}
        {modelInfo && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">Model Information</h4>
            <div className="text-xs text-muted-foreground space-y-1">
              <p>ID: {modelInfo.model_id}</p>
              <p>Prompt: {modelInfo.prompt}</p>
              <p>Created: {new Date(modelInfo.created_at).toLocaleString()}</p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
