import { useState, useEffect, useRef } from 'react'
import { Play, Pause, SkipBack, SkipForward, Volume2, Settings, Wifi, WifiOff, Camera, Video, Phone } from 'lucide-react'
import { Button } from "/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "/components/ui/card"
import { Slider } from "/components/ui/slider"
import { Label } from "/components/ui/label"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "/components/ui/tabs"

export default function SmartGlassesControl() {
  const [isPlaying, setIsPlaying] = useState(false)
  const [volume, setVolume] = useState(50)
  const [isConnected, setIsConnected] = useState(true)
  const [brightness, setBrightness] = useState(70)
  const [contrast, setContrast] = useState(50)
  const [activeTab, setActiveTab] = useState('media')
  const [cameraActive, setCameraActive] = useState(false)
  const [videoCallActive, setVideoCallActive] = useState(false)
  const videoRef = useRef<HTMLVideoElement>(null)

  // Simulate connection status changes
  useEffect(() => {
    const interval = setInterval(() => {
      if (Math.random() < 0.1) {
        setIsConnected(prev => !prev)
      }
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  // Load settings from localStorage
  useEffect(() => {
    const savedBrightness = localStorage.getItem('brightness')
    const savedContrast = localStorage.getItem('contrast')
    if (savedBrightness) setBrightness(Number(savedBrightness))
    if (savedContrast) setContrast(Number(savedContrast))
  }, [])

  // Save settings to localStorage when changed
  useEffect(() => {
    localStorage.setItem('brightness', brightness.toString())
    localStorage.setItem('contrast', contrast.toString())
  }, [brightness, contrast])

  const handleReconnect = () => {
    setIsConnected(false)
    setTimeout(() => setIsConnected(true), 1500)
  }

  const toggleCamera = () => {
    setCameraActive(!cameraActive)
    if (videoCallActive) setVideoCallActive(false)
    
    // In a real app, this would access the device camera
    if (!cameraActive && videoRef.current) {
      // Simulate camera feed
      videoRef.current.srcObject = new MediaStream()
    }
  }

  const toggleVideoCall = () => {
    setVideoCallActive(!videoCallActive)
    if (cameraActive) setCameraActive(false)
    
    if (!videoCallActive && videoRef.current) {
      // Simulate video call feed
      videoRef.current.srcObject = new MediaStream()
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>Smart Glasses Control</CardTitle>
            <div className="flex gap-2">
              <Button 
                variant={cameraActive ? "default" : "outline"} 
                size="icon" 
                onClick={toggleCamera}
                disabled={!isConnected}
              >
                <Camera className="h-5 w-5" />
              </Button>
              <Button 
                variant={videoCallActive ? "default" : "outline"} 
                size="icon" 
                onClick={toggleVideoCall}
                disabled={!isConnected}
              >
                <Phone className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Connection Status */}
          <div className="flex items-center gap-2">
            {isConnected ? (
              <>
                <Wifi className="h-5 w-5 text-green-500" />
                <span className="text-green-500">Connected</span>
              </>
            ) : (
              <>
                <WifiOff className="h-5 w-5 text-red-500" />
                <span className="text-red-500">Disconnected</span>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="ml-auto"
                  onClick={handleReconnect}
                >
                  Reconnect
                </Button>
              </>
            )}
          </div>

          {/* Camera/Video Preview */}
          {(cameraActive || videoCallActive) && (
            <div className="relative bg-black rounded-lg aspect-video flex items-center justify-center">
              <video 
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-full object-cover rounded-lg"
              />
              <div className="absolute inset-0 flex items-center justify-center">
                {videoCallActive && (
                  <div className="text-white bg-black bg-opacity-50 p-2 rounded-lg">
                    Video Call Active
                  </div>
                )}
              </div>
            </div>
          )}

          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="media">Media</TabsTrigger>
              <TabsTrigger value="settings">Settings</TabsTrigger>
            </TabsList>

            <TabsContent value="media">
              {/* Media Controls */}
              <div className="flex justify-center gap-4 mt-4">
                <Button variant="outline" size="icon" className="h-12 w-12" disabled={!isConnected}>
                  <SkipBack className="h-5 w-5" />
                </Button>
                <Button 
                  variant="default" 
                  size="icon" 
                  className="h-12 w-12"
                  onClick={() => setIsPlaying(!isPlaying)}
                  disabled={!isConnected}
                >
                  {isPlaying ? (
                    <Pause className="h-5 w-5" />
                  ) : (
                    <Play className="h-5 w-5" />
                  )}
                </Button>
                <Button variant="outline" size="icon" className="h-12 w-12" disabled={!isConnected}>
                  <SkipForward className="h-5 w-5" />
                </Button>
              </div>

              {/* Volume Control */}
              <div className="space-y-2 mt-6">
                <div className="flex items-center gap-2">
                  <Volume2 className="h-5 w-5 text-gray-500" />
                  <Label>Volume</Label>
                </div>
                <Slider 
                  value={[volume]} 
                  onValueChange={(value) => setVolume(value[0])}
                  max={100}
                  step={1}
                  disabled={!isConnected}
                />
                <div className="text-sm text-gray-500 text-right">{volume}%</div>
              </div>
            </TabsContent>

            <TabsContent value="settings">
              <div className="space-y-4 pt-2">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label>Brightness</Label>
                    <span className="text-sm text-gray-500">{brightness}%</span>
                  </div>
                  <Slider 
                    value={[brightness]} 
                    onValueChange={(value) => setBrightness(value[0])}
                    max={100}
                    step={5}
                  />
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label>Contrast</Label>
                    <span className="text-sm text-gray-500">{contrast}%</span>
                  </div>
                  <Slider 
                    value={[contrast]} 
                    onValueChange={(value) => setContrast(value[0])}
                    max={100}
                    step={5}
                  />
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>

        <CardFooter className="text-xs text-gray-500">
          Smart Glasses v2.0 with Camera
        </CardFooter>
      </Card>
    </div>
  )
}