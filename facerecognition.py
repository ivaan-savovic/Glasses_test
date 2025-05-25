import { useState, useEffect, useRef } from 'react';
import { Camera, Search, User, Settings, Wifi, WifiOff, X, Check, Loader2 } from 'lucide-react';
import { Button } from "/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "/components/ui/tabs";
import { Input } from "/components/ui/input";
import { Avatar, AvatarImage, AvatarFallback } from "/components/ui/avatar";

type SocialMediaProfile = {
  id: string;
  name: string;
  handle: string;
  platform: 'facebook' | 'instagram' | 'twitter' | 'linkedin';
  avatar: string;
  matchConfidence: number;
  lastSeen: string;
};

export default function AutoFaceRecognitionApp() {
  const [isConnected, setIsConnected] = useState(true);
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<SocialMediaProfile[] | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('scan');
  const [scanStatus, setScanStatus] = useState<'idle' | 'scanning' | 'detected' | 'searching' | 'complete'>('idle');
  const [faceDetected, setFaceDetected] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const detectionInterval = useRef<NodeJS.Timeout | null>(null);

  // Simulate connection status
  useEffect(() => {
    const interval = setInterval(() => {
      if (Math.random() < 0.1) {
        setIsConnected(prev => !prev);
      }
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Initialize camera
  useEffect(() => {
    if (activeTab === 'scan' && isScanning) {
      startCamera();
    } else {
      stopCamera();
    }

    return () => {
      stopCamera();
    };
  }, [activeTab, isScanning]);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          facingMode: 'user',
          width: { ideal: 1280 },
          height: { ideal: 720 }
        } 
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      
      startFaceDetection();
      setScanStatus('scanning');
    } catch (err) {
      console.error("Camera error:", err);
      setScanStatus('idle');
      setIsScanning(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    
    if (detectionInterval.current) {
      clearInterval(detectionInterval.current);
      detectionInterval.current = null;
    }
    
    setFaceDetected(false);
  };

  const startFaceDetection = () => {
    // In a real app, you would use a proper face detection library
    // Here we simulate face detection with random detection
    detectionInterval.current = setInterval(() => {
      // 20% chance to "detect" a face for demo purposes
      if (Math.random() < 0.2 && !faceDetected) {
        setFaceDetected(true);
        setScanStatus('detected');
        simulateFaceRecognition();
      }
    }, 2000);
  };

  const simulateFaceRecognition = () => {
    setScanStatus('searching');
    
    // Simulate network request delay
    setTimeout(() => {
      // Mock data for demonstration
      setScanResult([
        {
          id: '1',
          name: 'Emma Wilson',
          handle: '@emmawilson',
          platform: 'instagram',
          avatar: '',
          matchConfidence: 94,
          lastSeen: '2 hours ago'
        },
        {
          id: '2',
          name: 'Emma Wilson',
          handle: 'emma.wilson.92',
          platform: 'facebook',
          avatar: '',
          matchConfidence: 89,
          lastSeen: '1 day ago'
        },
        {
          id: '3',
          name: 'Emma W.',
          handle: '@emma_tech',
          platform: 'twitter',
          avatar: '',
          matchConfidence: 81,
          lastSeen: '3 hours ago'
        }
      ]);
      setScanStatus('complete');
    }, 3000);
  };

  const handleReconnect = () => {
    setIsConnected(false);
    setTimeout(() => setIsConnected(true), 1500);
  };

  const startFaceScan = () => {
    if (!isConnected) return;
    setIsScanning(true);
    setScanResult(null);
    setFaceDetected(false);
  };

  const stopFaceScan = () => {
    setIsScanning(false);
    setScanStatus('idle');
    setFaceDetected(false);
  };

  const handleSearch = () => {
    if (!searchQuery.trim()) return;
    
    setScanStatus('searching');
    setTimeout(() => {
      // Mock data for demonstration
      setScanResult([
        {
          id: '4',
          name: searchQuery,
          handle: `@${searchQuery.toLowerCase()}`,
          platform: 'instagram',
          avatar: '',
          matchConfidence: 85,
          lastSeen: '5 hours ago'
        },
        {
          id: '5',
          name: `${searchQuery} Johnson`,
          handle: `${searchQuery.toLowerCase()}.johnson`,
          platform: 'facebook',
          avatar: '',
          matchConfidence: 78,
          lastSeen: '1 week ago'
        }
      ]);
      setScanStatus('complete');
    }, 2000);
  };

  const getPlatformColor = (platform: string) => {
    switch (platform) {
      case 'facebook': return 'bg-blue-600';
      case 'instagram': return 'bg-gradient-to-r from-purple-500 to-pink-500';
      case 'twitter': return 'bg-blue-400';
      case 'linkedin': return 'bg-blue-700';
      default: return 'bg-gray-500';
    }
  };

  const getPlatformName = (platform: string) => {
    switch (platform) {
      case 'facebook': return 'Facebook';
      case 'instagram': return 'Instagram';
      case 'twitter': return 'Twitter';
      case 'linkedin': return 'LinkedIn';
      default: return platform;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>Auto Face Recognition</CardTitle>
            <div className="flex gap-2">
              <Button 
                variant={isScanning ? "default" : "outline"} 
                size="icon" 
                onClick={isScanning ? stopFaceScan : startFaceScan}
                disabled={!isConnected || activeTab !== 'scan'}
              >
                {isScanning ? <X className="h-5 w-5" /> : <Camera className="h-5 w-5" />}
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

          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="scan">Auto Scan</TabsTrigger>
              <TabsTrigger value="search">Manual Search</TabsTrigger>
            </TabsList>

            <TabsContent value="scan">
              {/* Face Scan Interface */}
              <div className="relative bg-black rounded-lg aspect-video flex items-center justify-center mt-4 overflow-hidden">
                {isScanning ? (
                  <>
                    <video 
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      className="w-full h-full object-cover"
                    />
                    <canvas 
                      ref={canvasRef}
                      className="absolute inset-0 w-full h-full pointer-events-none"
                    />
                    
                    {/* Detection indicator */}
                    {faceDetected && (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="animate-pulse border-4 border-green-500 rounded-full h-32 w-32 md:h-48 md:w-48 flex items-center justify-center">
                          <Check className="h-12 w-12 text-green-500" />
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="text-white text-center p-4">
                    <Camera className="h-12 w-12 mx-auto mb-2" />
                    <p>Press camera button to start</p>
                    <p className="text-sm text-gray-300 mt-2">Face recognition will work automatically</p>
                  </div>
                )}
              </div>

              {/* Status indicator */}
              {isScanning && (
                <div className="mt-2 text-center">
                  {scanStatus === 'scanning' && !faceDetected && (
                    <div className="flex items-center justify-center text-blue-500">
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      <span>Looking for faces...</span>
                    </div>
                  )}
                  {scanStatus === 'detected' && (
                    <div className="text-green-500">
                      <Check className="h-4 w-4 inline mr-2" />
                      <span>Face detected</span>
                    </div>
                  )}
                  {scanStatus === 'searching' && (
                    <div className="flex items-center justify-center text-blue-500">
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      <span>Searching social networks...</span>
                    </div>
                  )}
                </div>
              )}
            </TabsContent>

            <TabsContent value="search">
              {/* Manual Search Interface */}
              <div className="mt-4 space-y-4">
                <div className="flex gap-2">
                  <Input 
                    placeholder="Enter name or username" 
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                  />
                  <Button onClick={handleSearch} disabled={!isConnected || !searchQuery.trim()}>
                    <Search className="h-4 w-4 mr-2" />
                    Search
                  </Button>
                </div>
                
                {scanStatus === 'searching' && (
                  <div className="text-center py-8">
                    <div className="animate-pulse">
                      <Search className="h-8 w-8 mx-auto mb-2" />
                    </div>
                    <p>Searching social networks...</p>
                  </div>
                )}
              </div>
            </TabsContent>
          </Tabs>

          {/* Results Section */}
          {(scanResult && scanStatus === 'complete') && (
            <div className="mt-6">
              <h3 className="font-medium mb-3">Matching Profiles:</h3>
              <div className="space-y-3">
                {scanResult.map((profile) => (
                  <div key={profile.id} className="flex items-start p-3 border rounded-lg hover:bg-gray-50 transition-colors">
                    <Avatar className="h-10 w-10 mr-3 mt-1">
                      <AvatarImage src={profile.avatar} />
                      <AvatarFallback className={getPlatformColor(profile.platform)}>
                        {profile.name.charAt(0)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium truncate">{profile.name}</p>
                      <p className="text-sm text-gray-500 truncate">{profile.handle}</p>
                      <div className="flex items-center mt-1">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          profile.matchConfidence > 85 ? 'bg-green-100 text-green-800' :
                          profile.matchConfidence > 75 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {profile.matchConfidence}% match
                        </span>
                        <span className="text-xs text-gray-500 ml-2">
                          {getPlatformName(profile.platform)} • {profile.lastSeen}
                        </span>
                      </div>
                    </div>
                    <Button variant="outline" size="sm" className="ml-2">
                      View
                    </Button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>

        <CardFooter className="text-xs text-gray-500">
          Auto Face Recognition Social v1.0
        </CardFooter>
      </Card>
    </div>
  );
}