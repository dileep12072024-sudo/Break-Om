'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Progress } from '@/components/ui/progress'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useDropzone } from 'react-dropzone'
import { Upload, Wand2, Image as ImageIcon, Loader2 } from 'lucide-react'
import { toast } from 'sonner'
import axios from 'axios'

const generationSchema = z.object({
  prompt: z.string().min(1, 'Prompt is required').max(1000),
  generate_texture: z.boolean().default(true),
  format: z.enum(['glb', 'obj', 'fbx']).default('obj'),
})

type GenerationFormData = z.infer<typeof generationSchema>

interface ModelGeneratorProps {
  onModelGenerated: (modelId: string) => void
}

export function ModelGenerator({ onModelGenerated }: ModelGeneratorProps) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [generationMode, setGenerationMode] = useState<'text' | 'image'>('text')
  const [uploadedImage, setUploadedImage] = useState<File | null>(null)

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<GenerationFormData>({
    resolver: zodResolver(generationSchema),
    defaultValues: {
      prompt: '',
      generate_texture: true,
      format: 'obj',
    },
  })

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp'],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setUploadedImage(acceptedFiles[0])
      }
    },
  })

  const generate_texture = watch('generate_texture')
  const format = watch('format')

  const onSubmit = async (data: GenerationFormData) => {
    setIsGenerating(true)
    setProgress(0)

    try {
      const formData = new FormData()
      
      if (generationMode === 'text') {
        // Text-to-3D generation
        const response = await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/models/generate`,
          data,
          {
            headers: {
              'Content-Type': 'application/json',
            },
            onUploadProgress: (progressEvent) => {
              if (progressEvent.total) {
                const percentCompleted = Math.round(
                  (progressEvent.loaded * 100) / progressEvent.total
                )
                setProgress(percentCompleted)
              }
            },
          }
        )

        if (response.data.success) {
          toast.success('Model generated successfully!')
          onModelGenerated(response.data.model_id)
          // Reset form
          setValue('prompt', '')
          setUploadedImage(null)
        } else {
          toast.error(response.data.message || 'Generation failed')
        }
      } else {
        // Image-to-3D generation
        if (!uploadedImage) {
          toast.error('Please upload an image first')
          return
        }

        formData.append('file', uploadedImage)
        formData.append('generate_texture', data.generate_texture.toString())
        formData.append('format', data.format)

        const response = await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/models/generate-from-image`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
            onUploadProgress: (progressEvent) => {
              if (progressEvent.total) {
                const percentCompleted = Math.round(
                  (progressEvent.loaded * 100) / progressEvent.total
                )
                setProgress(percentCompleted)
              }
            },
          }
        )

        if (response.data.success) {
          toast.success('Model generated from image successfully!')
          onModelGenerated(response.data.model_id)
          setUploadedImage(null)
        } else {
          toast.error(response.data.message || 'Generation failed')
        }
      }
    } catch (error: any) {
      console.error('Generation error:', error)
      toast.error(
        error.response?.data?.detail || 
        error.message || 
        'Failed to generate model'
      )
    } finally {
      setIsGenerating(false)
      setProgress(0)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Wand2 className="h-5 w-5" />
          Generate 3D Model
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Generation Mode Toggle */}
        <div className="flex gap-2">
          <Button
            variant={generationMode === 'text' ? 'default' : 'outline'}
            onClick={() => setGenerationMode('text')}
            className="flex-1"
          >
            <ImageIcon className="h-4 w-4 mr-2" />
            Text to 3D
          </Button>
          <Button
            variant={generationMode === 'image' ? 'default' : 'outline'}
            onClick={() => setGenerationMode('image')}
            className="flex-1"
          >
            <Upload className="h-4 w-4 mr-2" />
            Image to 3D
          </Button>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {generationMode === 'text' ? (
            /* Text Input */
            <div className="space-y-2">
              <Label htmlFor="prompt">Prompt</Label>
              <Textarea
                id="prompt"
                placeholder="Describe the 3D model you want to generate..."
                className="min-h-[100px]"
                {...register('prompt')}
              />
              {errors.prompt && (
                <p className="text-sm text-destructive">{errors.prompt.message}</p>
              )}
            </div>
          ) : (
            /* Image Upload */
            <div className="space-y-2">
              <Label>Upload Image</Label>
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                  isDragActive
                    ? 'border-primary bg-primary/10'
                    : 'border-muted-foreground/25 hover:border-muted-foreground/50'
                }`}
              >
                <input {...getInputProps()} />
                <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                {isDragActive ? (
                  <p>Drop the image here...</p>
                ) : uploadedImage ? (
                  <div className="space-y-2">
                    <p className="text-sm font-medium">{uploadedImage.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {(uploadedImage.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <p>Drag & drop an image here, or click to select</p>
                    <p className="text-xs text-muted-foreground">
                      Supports: JPEG, PNG, WebP (max 10MB)
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Generation Options */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label htmlFor="generate_texture">Generate Texture</Label>
              <Switch
                id="generate_texture"
                checked={generate_texture}
                onCheckedChange={(checked) => setValue('generate_texture', checked)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="format">Output Format</Label>
              <Select
                value={format}
                onValueChange={(value: 'glb' | 'obj' | 'fbx') => setValue('format', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select format" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="glb">GLB (Recommended)</SelectItem>
                  <SelectItem value="obj">OBJ</SelectItem>
                  <SelectItem value="fbx">FBX</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Progress */}
          {isGenerating && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Generating model...</span>
                <span>{progress}%</span>
              </div>
              <Progress value={progress} className="w-full" />
            </div>
          )}

          {/* Submit Button */}
          <Button
            type="submit"
            disabled={isGenerating || (generationMode === 'image' && !uploadedImage)}
            className="w-full"
          >
            {isGenerating ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Wand2 className="h-4 w-4 mr-2" />
                Generate Model
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
