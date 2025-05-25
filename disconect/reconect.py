import { useState, useEffect } from 'react'
import { Play, Pause, SkipBack, SkipForward, Volume2, Settings, Wifi, WifiOff } from 'lucide-react'
import { Button } from "/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "/components/ui/card"
import { Slider } from "/components/ui/slider"
import { Label } from "/components/ui/label"
import { Switch } from "/components/ui/switch"

export default function SmartGlassesControl() {
  const [isPlaying, setIsPlaying] = useState(false)
  const [volume, setVolume] = useState(50)
  const [isConnected, setIsConnected] = useState(true)
  const [showSettings, setShowSettings] = useState(false)
  const [brightness, setBrightness] = useState(70)
  const [contrast, setContrast] = useState(50)

  // Simulate connection status changes
  useEffect(() => {
    const interval = setInterval(() => {
      // 10% chance to toggle connection status for demo purposes
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
    // Simulate reconnection after 1.5 seconds
    setTimeout(() => setIsConnected(true), 1500)
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>Smart Glasses Control</CardTitle>
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={() => setShowSettings(!showSettings)}
            >
              <Settings className="h-5 w-5" />
            </Button>
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

          {/* Media Controls */}
          <div className="flex justify-center gap-4">
            <Button variant="outline" size="icon" className="h-12 w-12">
              <SkipBack className="h-5 w-5" />
            </Button>
            <Button 
              variant="default" 
              size="icon" 
              className="h-12 w-12"
              onClick={() => setIsPlaying(!isPlaying)}
            >
              {isPlaying ? (
                <Pause className="h-5 w-5" />
              ) : (
                <Play className="h-5 w-5" />
              )}
            </Button>
            <Button variant="outline" size="icon" className="h-12 w-12">
              <SkipForward className="h-5 w-5" />
            </Button>
          </div>

          {/* Volume Control */}
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <Volume2 className="h-5 w-5 text-gray-500" />
              <Label>Volume</Label>
            </div>
            <Slider 
              value={[volume]} 
              onValueChange={(value) => setVolume(value[0])}
              max={100}
              step={1}
            />
            <div className="text-sm text-gray-500 text-right">{volume}%</div>
          </div>

          {/* Settings Panel */}
          {showSettings && (
            <div className="space-y-4 pt-4 border-t">
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
          )}
        </CardContent>

        <CardFooter className="text-xs text-gray-500">
          Smart Glasses v1.0
        </CardFooter>
      </Card>
    </div>
  )
}