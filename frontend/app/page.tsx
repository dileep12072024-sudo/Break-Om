'use client'

import { useState } from 'react'
import { ModelGenerator } from '@/components/ModelGenerator'
import { ModelViewer } from '@/components/ModelViewer'
import { ModelGallery } from '@/components/ModelGallery'
import { Header } from '@/components/Header'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

export default function Home() {
  const [currentModel, setCurrentModel] = useState<string | null>(null)
  const [refreshGallery, setRefreshGallery] = useState(0)

  const handleModelGenerated = (modelId: string) => {
    setCurrentModel(modelId)
    setRefreshGallery(prev => prev + 1)
  }

  const handleModelSelected = (modelId: string) => {
    setCurrentModel(modelId)
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Panel - Generation and Gallery */}
          <div className="space-y-6">
            <Tabs defaultValue="generate" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="generate">Generate</TabsTrigger>
                <TabsTrigger value="gallery">Gallery</TabsTrigger>
              </TabsList>
              
              <TabsContent value="generate" className="space-y-4">
                <ModelGenerator onModelGenerated={handleModelGenerated} />
              </TabsContent>
              
              <TabsContent value="gallery" className="space-y-4">
                <ModelGallery 
                  onModelSelected={handleModelSelected}
                  refreshTrigger={refreshGallery}
                />
              </TabsContent>
            </Tabs>
          </div>

          {/* Right Panel - 3D Viewer */}
          <div className="space-y-6">
            <div className="h-[600px]">
              <ModelViewer modelId={currentModel} />
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
