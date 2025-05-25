import { useState, useEffect, useRef } from 'react'
import { Button } from "/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "/components/ui/card"
import { Input } from "/components/ui/input"
import { Label } from "/components/ui/label"
import { Clock, CloudSun, Newspaper, MessageSquare, Search, Calendar, User, Settings, Mail, Home, Play, Plus, Minus, Check, X, Camera, Video } from 'lucide-react'

export default function SmartGlassesAssistant() {
  const [isListening, setIsListening] = useState(false)
  const [command, setCommand] = useState('')
  const [response, setResponse] = useState('')
  const [currentTime, setCurrentTime] = useState('')
  const [currentDate, setCurrentDate] = useState('')
  const [weather, setWeather] = useState({ temp: '72°F', condition: 'Sunny', location: 'New York' })
  const [news, setNews] = useState([
    'Scientists discover new species in Amazon',
    'Tech company announces breakthrough in AI',
    'Local community raises funds for school'
  ])
  const [reminders, setReminders] = useState<string[]>([])
  const [newReminder, setNewReminder] = useState('')
  const [contacts, setContacts] = useState([
    { name: 'John Doe', number: '555-1234', online: true },
    { name: 'Jane Smith', number: '555-5678', online: false }
  ])
  const [smsRecipient, setSmsRecipient] = useState('')
  const [smsMessage, setSmsMessage] = useState('')
  const [showSmsForm, setShowSmsForm] = useState(false)
  const [activeDisplay, setActiveDisplay] = useState<'time' | 'weather' | 'news' | 'reminders' | 'contacts' | 'camera' | 'video'>('time')
  const [volume, setVolume] = useState(70)
  const [brightness, setBrightness] = useState(80)
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)
  const [isCameraActive, setIsCameraActive] = useState(false)
  const [isVideoCallActive, setIsVideoCallActive] = useState(false)
  const [currentPhoto, setCurrentPhoto] = useState<string | null>(null)
  const [videoCallContact, setVideoCallContact] = useState<string | null>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const commandInputRef = useRef<HTMLInputElement>(null)

  // Update time and date every second
  useEffect(() => {
    const updateDateTime = () => {
      const now = new Date()
      setCurrentTime(now.toLocaleTimeString())
      setCurrentDate(now.toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }))
    }
    updateDateTime()
    const timer = setInterval(updateDateTime, 1000)
    return () => clearInterval(timer)
  }, [])

  // Handle camera stream
  useEffect(() => {
    if (isCameraActive && videoRef.current) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream
          }
        })
        .catch(err => {
          console.error("Camera error: ", err)
          setResponse("Could not access camera. Please check permissions.")
          setIsCameraActive(false)
          setActiveDisplay('time')
        })
    }

    return () => {
      if (videoRef.current?.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream
        stream.getTracks().forEach(track => track.stop())
      }
    }
  }, [isCameraActive])

  // Focus command input when not listening
  useEffect(() => {
    if (!isListening && commandInputRef.current) {
      commandInputRef.current.focus()
    }
  }, [isListening])

  const handleVoiceCommand = () => {
    if (isListening) {
      setIsListening(false)
      if (command.trim()) {
        processCommand(command)
      }
      return
    }

    setIsListening(true)
    setCommand('')
    setResponse('Listening... Speak now')
  }

  const processCommand = (cmd: string) => {
    const lowerCmd = cmd.toLowerCase()
    setResponse('')

    if (lowerCmd.includes('time') || lowerCmd.includes('clock')) {
      setActiveDisplay('time')
      setResponse(`The current time is ${currentTime}`)
    } 
    else if (lowerCmd.includes('date') || lowerCmd.includes('today')) {
      setActiveDisplay('time')
      setResponse(`Today is ${currentDate}`)
    }
    else if (lowerCmd.includes('weather') || lowerCmd.includes('temperature')) {
      setActiveDisplay('weather')
      setResponse(`Current weather in ${weather.location}: ${weather.condition}, ${weather.temp}`)
    } 
    else if (lowerCmd.includes('news') || lowerCmd.includes('headlines')) {
      setActiveDisplay('news')
      setResponse(`Here are the latest news headlines`)
    } 
    else if (lowerCmd.includes('remind') || lowerCmd.includes('reminder')) {
      setActiveDisplay('reminders')
      if (lowerCmd.includes('add') || lowerCmd.includes('create') || lowerCmd.includes('new')) {
        const reminderText = cmd.replace(/add|create|new|remind|reminder/gi, '').trim()
        if (reminderText) {
          addReminder(reminderText)
        } else {
          setResponse('What would you like to be reminded about?')
        }
      } else {
        setResponse(`You have ${reminders.length} reminders`)
      }
    }
    else if (lowerCmd.includes('contact') || lowerCmd.includes('contacts')) {
      setActiveDisplay('contacts')
      setResponse(`Showing your contacts`)
    }
    else if (lowerCmd.includes('text') || lowerCmd.includes('message') || lowerCmd.includes('sms')) {
      const contactMatch = contacts.find(c => 
        lowerCmd.includes(c.name.toLowerCase()) || 
        lowerCmd.includes(c.number.replace('-', ''))
      )
      
      if (contactMatch) {
        setSmsRecipient(contactMatch.number)
        const messageText = cmd.replace(/text|message|sms/gi, '')
                             .replace(contactMatch.name, '')
                             .replace(contactMatch.number, '')
                             .trim()
        if (messageText) {
          setSmsMessage(messageText)
          handleSendSms()
        } else {
          setShowSmsForm(true)
          setResponse(`What would you like to send to ${contactMatch.name}?`)
        }
      } else {
        setShowSmsForm(true)
        setResponse('Who would you like to message?')
      }
    }
    else if (lowerCmd.includes('photo') || lowerCmd.includes('picture') || lowerCmd.includes('camera')) {
      setActiveDisplay('camera')
      setIsCameraActive(true)
      setResponse('Camera activated. Say "take photo" to capture.')
    }
    else if (lowerCmd.includes('take photo') || lowerCmd.includes('capture')) {
      if (isCameraActive) {
        takePhoto()
      } else {
        setResponse('Please activate camera first')
      }
    }
    else if (lowerCmd.includes('video call') || lowerCmd.includes('call')) {
      const contactMatch = contacts.find(c => 
        lowerCmd.includes(c.name.toLowerCase()) || 
        lowerCmd.includes(c.number.replace('-', ''))
      )
      
      if (contactMatch) {
        if (contactMatch.online) {
          setVideoCallContact(contactMatch.name)
          setActiveDisplay('video')
          setIsVideoCallActive(true)
          setResponse(`Calling ${contactMatch.name}...`)
        } else {
          setResponse(`${contactMatch.name} is offline`)
        }
      } else {
        setResponse('Who would you like to call?')
      }
    }
    else if (lowerCmd.includes('end call') || lowerCmd.includes('hang up')) {
      if (isVideoCallActive) {
        endVideoCall()
      }
    }
    else if (lowerCmd.includes('hello') || lowerCmd.includes('hi')) {
      setResponse('Hello! How can I assist you today?')
    }
    else if (lowerCmd.includes('help') || lowerCmd.includes('what can you do')) {
      setResponse('I can show time, weather, news, reminders, contacts, send messages, take photos, and make video calls. Try saying "what time is it?" or "call John"')
    }
    else if (lowerCmd.includes('settings') || lowerCmd.includes('brightness') || lowerCmd.includes('volume')) {
      setIsSettingsOpen(true)
      setResponse('Opening settings')
    }
    else {
      setResponse(`I didn't understand that. Try asking about time, weather, news, or say "help"`)
    }
  }

  const takePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d')
      if (context) {
        canvasRef.current.width = videoRef.current.videoWidth
        canvasRef.current.height = videoRef.current.videoHeight
        context.drawImage(videoRef.current, 0, 0)
        const photoData = canvasRef.current.toDataURL('image/png')
        setCurrentPhoto(photoData)
        setResponse('Photo captured!')
      }
    }
  }

  const savePhoto = () => {
    if (currentPhoto) {
      // In a real app, you would save to storage
      setResponse('Photo saved to gallery')
    }
  }

  const discardPhoto = () => {
    setCurrentPhoto(null)
    setResponse('Photo discarded')
  }

  const endVideoCall = () => {
    setIsVideoCallActive(false)
    setVideoCallContact(null)
    setActiveDisplay('time')
    setResponse('Call ended')
  }

  const addReminder = (text: string) => {
    setReminders([...reminders, text])
    setResponse(`Added reminder: "${text}"`)
  }

  const removeReminder = (index: number) => {
    const newReminders = [...reminders]
    newReminders.splice(index, 1)
    setReminders(newReminders)
  }

  const handleSendSms = () => {
    if (!smsRecipient) {
      setResponse('Please enter a recipient')
      return
    }
    if (!smsMessage) {
      setResponse('Please enter a message')
      return
    }

    const contact = contacts.find(c => c.number === smsRecipient)
    setResponse(`Message sent to ${contact ? contact.name : smsRecipient}: "${smsMessage}"`)
    setSmsRecipient('')
    setSmsMessage('')
    setShowSmsForm(false)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && command.trim()) {
      processCommand(command)
      setCommand('')
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="text-2xl font-bold">Smart Glasses Assistant</CardTitle>
              <CardDescription>Voice-activated assistant</CardDescription>
            </div>
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={() => setIsSettingsOpen(!isSettingsOpen)}
            >
              <Settings className="h-5 w-5" />
            </Button>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Settings Panel */}
          {isSettingsOpen && (
            <div className="bg-gray-50 p-4 rounded-lg space-y-4">
              <h3 className="font-semibold flex items-center">
                <Settings className="mr-2 h-5 w-5" /> Settings
              </h3>
              
              <div>
                <Label>Volume: {volume}%</Label>
                <div className="flex items-center gap-2">
                  <Button variant="outline" size="sm" onClick={() => setVolume(Math.max(0, volume - 10))}>
                    <Minus className="h-4 w-4" />
                  </Button>
                  <div className="flex-1 h-2 bg-gray-200 rounded-full">
                    <div 
                      className="h-full bg-blue-500 rounded-full" 
                      style={{ width: `${volume}%` }}
                    ></div>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => setVolume(Math.min(100, volume + 10))}>
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <div>
                <Label>Brightness: {brightness}%</Label>
                <div className="flex items-center gap-2">
                  <Button variant="outline" size="sm" onClick={() => setBrightness(Math.max(0, brightness - 10))}>
                    <Minus className="h-4 w-4" />
                  </Button>
                  <div className="flex-1 h-2 bg-gray-200 rounded-full">
                    <div 
                      className="h-full bg-yellow-500 rounded-full" 
                      style={{ width: `${brightness}%` }}
                    ></div>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => setBrightness(Math.min(100, brightness + 10))}>
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <Button 
                variant="secondary" 
                className="w-full"
                onClick={() => setIsSettingsOpen(false)}
              >
                <Check className="mr-2 h-4 w-4" /> Done
              </Button>
            </div>
          )}

          {/* Display Area */}
          <div className="bg-gray-50 rounded-lg p-4 h-64 flex flex-col">
            <div className="flex justify-between items-center mb-2">
              <div className="text-sm text-gray-500">
                {activeDisplay === 'time' && <Clock className="inline mr-1 h-4 w-4" />}
                {activeDisplay === 'weather' && <CloudSun className="inline mr-1 h-4 w-4" />}
                {activeDisplay === 'news' && <Newspaper className="inline mr-1 h-4 w-4" />}
                {activeDisplay === 'reminders' && <Calendar className="inline mr-1 h-4 w-4" />}
                {activeDisplay === 'contacts' && <User className="inline mr-1 h-4 w-4" />}
                {activeDisplay === 'camera' && <Camera className="inline mr-1 h-4 w-4" />}
                {activeDisplay === 'video' && <Video className="inline mr-1 h-4 w-4" />}
                {activeDisplay.charAt(0).toUpperCase() + activeDisplay.slice(1)}
              </div>
              <div className="text-sm text-gray-500">{currentTime}</div>
            </div>

            <div className="flex-1 overflow-auto">
              {activeDisplay === 'time' && (
                <div className="text-center space-y-2">
                  <p className="text-4xl font-bold">{currentTime}</p>
                  <p className="text-lg">{currentDate}</p>
                </div>
              )}

              {activeDisplay === 'weather' && (
                <div className="text-center space-y-2">
                  <CloudSun className="h-12 w-12 mx-auto" />
                  <p className="text-3xl font-bold">{weather.temp}</p>
                  <p className="text-xl">{weather.condition}</p>
                  <p className="text-gray-600">{weather.location}</p>
                </div>
              )}

              {activeDisplay === 'news' && (
                <div className="space-y-3">
                  {news.map((item, index) => (
                    <div key={index} className="p-2 bg-white rounded">
                      <p>{item}</p>
                    </div>
                  ))}
                </div>
              )}

              {activeDisplay === 'reminders' && (
                <div className="space-y-2">
                  {reminders.length === 0 ? (
                    <p className="text-center text-gray-500 py-4">No reminders</p>
                  ) : (
                    reminders.map((reminder, index) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-white rounded">
                        <p>{reminder}</p>
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={() => removeReminder(index)}
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    ))
                  )}
                  <div className="flex gap-2 mt-2">
                    <Input
                      value={newReminder}
                      onChange={(e) => setNewReminder(e.target.value)}
                      placeholder="New reminder..."
                    />
                    <Button 
                      onClick={() => {
                        if (newReminder.trim()) {
                          addReminder(newReminder)
                          setNewReminder('')
                        }
                      }}
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}

              {activeDisplay === 'contacts' && (
                <div className="space-y-2">
                  {contacts.map((contact, index) => (
                    <div 
                      key={index} 
                      className="flex items-center justify-between p-3 bg-white rounded hover:bg-gray-50 cursor-pointer"
                      onClick={() => {
                        setSmsRecipient(contact.number)
                        setShowSmsForm(true)
                      }}
                    >
                      <div>
                        <p className="font-medium">{contact.name}</p>
                        <p className="text-sm text-gray-600">{contact.number}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`h-2 w-2 rounded-full ${contact.online ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                        <MessageSquare className="h-5 w-5 text-gray-400" />
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {activeDisplay === 'camera' && (
                <div className="relative h-full">
                  {currentPhoto ? (
                    <>
                      <img src={currentPhoto} alt="Captured" className="w-full h-full object-contain" />
                      <div className="absolute bottom-0 left-0 right-0 flex justify-center gap-2 p-2 bg-black bg-opacity-50">
                        <Button variant="secondary" size="sm" onClick={savePhoto}>
                          <Check className="h-4 w-4 mr-1" /> Save
                        </Button>
                        <Button variant="destructive" size="sm" onClick={discardPhoto}>
                          <X className="h-4 w-4 mr-1" /> Discard
                        </Button>
                      </div>
                    </>
                  ) : (
                    <>
                      <video 
                        ref={videoRef} 
                        autoPlay 
                        playsInline 
                        muted 
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute bottom-0 left-0 right-0 flex justify-center p-2">
                        <Button 
                          onClick={takePhoto}
                          className="rounded-full h-12 w-12"
                        >
                          <Camera className="h-6 w-6" />
                        </Button>
                      </div>
                      <canvas ref={canvasRef} className="hidden" />
                    </>
                  )}
                </div>
              )}

              {activeDisplay === 'video' && (
                <div className="relative h-full bg-black rounded overflow-hidden">
                  {isVideoCallActive ? (
                    <>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="bg-gray-800 rounded-full h-24 w-24 flex items-center justify-center">
                          <User className="h-12 w-12 text-white" />
                        </div>
                      </div>
                      <div className="absolute bottom-0 left-0 right-0 p-4 bg-black bg-opacity-50 flex justify-center">
                        <Button 
                          variant="destructive" 
                          onClick={endVideoCall}
                          className="rounded-full h-12 w-12"
                        >
                          <X className="h-6 w-6" />
                        </Button>
                      </div>
                      <div className="absolute top-2 left-2 bg-black bg-opacity-50 text-white p-2 rounded">
                        <p>Calling: {videoCallContact}</p>
                      </div>
                    </>
                  ) : (
                    <div className="h-full flex items-center justify-center">
                      <p>Call ended</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Response Area */}
          {response && (
            <div className="bg-blue-50 p-3 rounded-lg border border-blue-100">
              <p className="text-blue-800">{response}</p>
            </div>
          )}

          {/* SMS Form */}
          {showSmsForm && (
            <div className="space-y-3">
              <div>
                <Label htmlFor="recipient">Recipient</Label>
                <Input
                  id="recipient"
                  value={smsRecipient}
                  onChange={(e) => setSmsRecipient(e.target.value)}
                  placeholder="Phone number"
                />
              </div>
              <div>
                <Label htmlFor="message">Message</Label>
                <Input
                  id="message"
                  value={smsMessage}
                  onChange={(e) => setSmsMessage(e.target.value)}
                  placeholder="Your message"
                />
              </div>
              <div className="flex gap-2">
                <Button onClick={handleSendSms} className="flex-1">
                  <MessageSquare className="mr-2 h-4 w-4" /> Send
                </Button>
                <Button variant="outline" onClick={() => setShowSmsForm(false)}>
                  Cancel
                </Button>
              </div>
            </div>
          )}

          {/* Command Input */}
          <div className="space-y-2">
            <Label htmlFor="command">Enter command</Label>
            <div className="flex gap-2">
              <Input
                ref={commandInputRef}
                id="command"
                value={command}
                onChange={(e) => setCommand(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={isListening ? "Listening..." : "Type a command or use voice..."}
                disabled={isListening}
              />
              <Button
                onClick={handleVoiceCommand}
                variant={isListening ? 'destructive' : 'default'}
                className="min-w-[100px]"
              >
                {isListening ? (
                  <>
                    <div className="h-2 w-2 rounded-full bg-white mr-2 animate-pulse"></div>
                    Stop
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" /> Voice
                  </>
                )}
              </Button>
            </div>
          </div>

          {/* Quick Command Buttons */}
          <div className="grid grid-cols-4 gap-2">
            <Button variant="outline" onClick={() => processCommand('time')} className="flex-col h-auto py-2">
              <Clock className="h-5 w-5 mb-1" />
              <span>Time</span>
            </Button>
            <Button variant="outline" onClick={() => processCommand('weather')} className="flex-col h-auto py-2">
              <CloudSun className="h-5 w-5 mb-1" />
              <span>Weather</span>
            </Button>
            <Button variant="outline" onClick={() => processCommand('news')} className="flex-col h-auto py-2">
              <Newspaper className="h-5 w-5 mb-1" />
              <span>News</span>
            </Button>
            <Button variant="outline" onClick={() => processCommand('reminders')} className="flex-col h-auto py-2">
              <Calendar className="h-5 w-5 mb-1" />
              <span>Reminders</span>
            </Button>
            <Button variant="outline" onClick={() => processCommand('contacts')} className="flex-col h-auto py-2">
              <User className="h-5 w-5 mb-1" />
              <span>Contacts</span>
            </Button>
            <Button variant="outline" onClick={() => processCommand('send message')} className="flex-col h-auto py-2">
              <MessageSquare className="h-5 w-5 mb-1" />
              <span>Message</span>
            </Button>
            <Button variant="outline" onClick={() => processCommand('camera')} className="flex-col h-auto py-2">
              <Camera className="h-5 w-5 mb-1" />
              <span>Camera</span>
            </Button>
            <Button variant="outline" onClick={() => processCommand('video call')} className="flex-col h-auto py-2">
              <Video className="h-5 w-5 mb-1" />
              <span>Video Call</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}