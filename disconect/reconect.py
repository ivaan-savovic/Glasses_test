import { useState, useEffect, useRef } from 'react'
import { Camera, Video, Phone, Loader2, X, Mic, MicOff, Bluetooth, User } from 'lucide-react'
import { Button } from "/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "/components/ui/card"
import { Avatar, AvatarFallback } from "/components/ui/avatar"
import { Progress } from "/components/ui/progress"

export default function BluetoothCameraControl() {
  const [isConnected, setIsConnected] = useState(false)
  const [isConnecting, setIsConnecting] = useState(false)
  const [cameraActive, setCameraActive] = useState(false)
  const [videoCallActive, setVideoCallActive] = useState(false)
  const [callStatus, setCallStatus] = useState<'idle' | 'ringing' | 'active'>('idle')
  const [isMuted, setIsMuted] = useState(false)
  const [batteryLevel, setBatteryLevel] = useState(85)
  const videoRef = useRef<HTMLVideoElement>(null)
  const callTimerRef = useRef<NodeJS.Timeout | null>(null)

  // Simulate Bluetooth connection
  const connectBluetooth = () => {
    setIsConnecting(true)
    setTimeout(() => {
      setIsConnected(true)
      setIsConnecting(false)
      setBatteryLevel(Math.floor(Math.random() * 30) + 70)
    }, 2000)
  }

  const disconnectBluetooth = () => {
    setIsConnected(false)
    setCameraActive(false)
    setVideoCallActive(false)
    setCallStatus('idle')
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream
      stream.getTracks().forEach(track => track.stop())
      videoRef.current.srcObject = null
    }
  }

  const toggleCamera = () => {
    if (videoCallActive) endVideoCall()
    setCameraActive(!cameraActive)
    
    if (!cameraActive && videoRef.current) {
      videoRef.current.srcObject = new MediaStream()
    } else if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream
      stream.getTracks().forEach(track => track.stop())
      videoRef.current.srcObject = null
    }
  }

  const startVideoCall = () => {
    setCallStatus('ringing')
    setTimeout(() => {
      setCallStatus('active')
      setVideoCallActive(true)
      if (videoRef.current) {
        videoRef.current.srcObject = new MediaStream()
      }
      callTimerRef.current = setTimeout(endVideoCall, 30000)
    }, 2000)
  }

  const endVideoCall = () => {
    setVideoCallActive(false)
    setCallStatus('idle')
    if (callTimerRef.current) clearTimeout(callTimerRef.current)
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream
      stream.getTracks().forEach(track => track.stop())
      videoRef.current.srcObject = null
    }
  }

  const handleCallAction = () => {
    if (callStatus === 'idle') {
      startVideoCall()
    } else {
      endVideoCall()
    }
  }

  const toggleMute = () => setIsMuted(!isMuted)

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>Bluetooth Glasses Control</CardTitle>
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-gray-300'}`}></div>
              <span className="text-sm">{isConnected ? 'Connected' : 'Disconnected'}</span>
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Bluetooth Connection Controls */}
          <div className="flex justify-between items-center bg-gray-100 p-3 rounded-lg">
            <div className="flex items-center gap-2">
              <Bluetooth className={`h-5 w-5 ${isConnected ? 'text-blue-500' : 'text-gray-500'}`} />
              <span className="text-sm">
                {isConnecting ? 'Connecting...' : isConnected ? 'Bluetooth Connected' : 'Not Connected'}
              </span>
            </div>
            {isConnected ? (
              <Button variant="outline" size="sm" onClick={disconnectBluetooth}>
                Disconnect
              </Button>
            ) : (
              <Button 
                variant="default" 
                size="sm" 
                onClick={connectBluetooth}
                disabled={isConnecting}
              >
                {isConnecting ? (
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                ) : null}
                Connect
              </Button>
            )}
          </div>

          {/* Battery Indicator */}
          <div className="flex items-center gap-3">
            <div className="w-full">
              <div className="flex justify-between text-xs mb-1">
                <span>Battery</span>
                <span>{batteryLevel}%</span>
              </div>
              <Progress value={batteryLevel} className="h-2" />
            </div>
          </div>

          {/* Camera/Video Preview */}
          <div className="relative bg-black rounded-lg aspect-video flex items-center justify-center">
            {(cameraActive || videoCallActive) ? (
              <>
                <video 
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className="w-full h-full object-cover rounded-lg"
                />
                <div className="absolute inset-0 flex flex-col items-center justify-between p-4">
                  {videoCallActive && (
                    <>
                      <div className="w-full flex justify-between">
                        <div className="text-white bg-black/50 p-2 rounded-lg text-sm">
                          {callStatus === 'active' ? "Call Active" : "Ringing..."}
                        </div>
                        <div className="text-white bg-black/50 p-2 rounded-lg text-sm">
                          00:30
                        </div>
                      </div>
                      <div className="flex gap-4">
                        <Button 
                          variant="outline" 
                          size="icon" 
                          className="bg-white/20 backdrop-blur-sm"
                          onClick={toggleMute}
                        >
                          {isMuted ? (
                            <MicOff className="h-5 w-5" />
                          ) : (
                            <Mic className="h-5 w-5" />
                          )}
                        </Button>
                        <Button 
                          variant="destructive" 
                          size="icon" 
                          onClick={endVideoCall}
                          className="bg-red-600/90 backdrop-blur-sm"
                        >
                          <Phone className="h-5 w-5" />
                        </Button>
                        <Button 
                          variant="outline" 
                          size="icon" 
                          className="bg-white/20 backdrop-blur-sm"
                        >
                          <Video className="h-5 w-5" />
                        </Button>
                      </div>
                    </>
                  )}
                  {cameraActive && (
                    <div className="absolute bottom-4 right-4">
                      <div className="bg-black/50 text-white p-2 rounded-lg text-sm">
                        Camera Active
                      </div>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div className="text-white text-center p-4">
                <Camera className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>{isConnected ? "Camera is off" : "Connect to enable"}</p>
              </div>
            )}
          </div>

          {/* Control Buttons */}
          <div className="flex justify-center gap-4">
            <Button 
              variant={cameraActive ? "default" : "outline"} 
              onClick={toggleCamera}
              disabled={!isConnected || videoCallActive}
              className="flex-1"
            >
              <Camera className="h-5 w-5 mr-2" />
              {cameraActive ? "Stop Camera" : "Start Camera"}
            </Button>
            <Button 
              variant={callStatus !== 'idle' ? "default" : "outline"} 
              onClick={handleCallAction}
              disabled={!isConnected || cameraActive}
              className="flex-1"
            >
              {callStatus === 'idle' ? (
                <>
                  <Phone className="h-5 w-5 mr-2" />
                  Video Call
                </>
              ) : callStatus === 'ringing' ? (
                <>
                  <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                  Ringing...
                </>
              ) : (
                <>
                  <Phone className="h-5 w-5 mr-2" />
                  End Call
                </>
              )}
            </Button>
          </div>

          {/* Call Ringing Indicator */}
          {callStatus === 'ringing' && !videoCallActive && (
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="flex items-center gap-4">
                <Avatar className="h-12 w-12">
                  <AvatarFallback className="bg-blue-100 text-blue-600">
                    <User className="h-6 w-6" />
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <h4 className="font-medium">Incoming Video Call</h4>
                  <p className="text-sm text-gray-500">Available Device</p>
                </div>
                <div className="flex gap-2">
                  <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={endVideoCall}
                    className="border-red-500 text-red-500 hover:bg-red-50"
                  >
                    <X className="h-4 w-4 mr-2" /> Decline
                  </Button>
                  <Button 
                    variant="default" 
                    size="sm" 
                    onClick={() => setCallStatus('active')}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    <Phone className="h-4 w-4 mr-2" /> Answer
                  </Button>
                </div>
              </div>
            </div>
          )}
        </CardContent>

        <CardFooter className="text-xs text-gray-500">
          Bluetooth Glasses Controller • v1.0
        </CardFooter>
      </Card>
    </div>
  )
}