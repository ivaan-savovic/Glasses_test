import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "/components/ui/card"
import { Button } from "/components/ui/button"
import { Thermometer, Droplets, Sun, Gauge, SunDim, Settings, X, Check } from "lucide-react"
import { Label } from "/components/ui/label"
import { Switch } from "/components/ui/switch"
import { Slider } from "/components/ui/slider"

type Sensor = {
  id: string
  name: string
  value: number
  unit: string
  icon: JSX.Element
  selected: boolean
  color: string
}

export default function SmartGlassesSensorApp() {
  const [sensors, setSensors] = useState<Sensor[]>([
    {
      id: 'temp',
      name: 'Temp',
      value: 22.5,
      unit: '°C',
      icon: <Thermometer className="w-5 h-5" />,
      selected: true,
      color: 'bg-amber-500'
    },
    {
      id: 'humidity',
      name: 'Humidity',
      value: 45,
      unit: '%',
      icon: <Droplets className="w-5 h-5" />,
      selected: true,
      color: 'bg-blue-500'
    },
    {
      id: 'light',
      name: 'Light',
      value: 750,
      unit: 'lux',
      icon: <Sun className="w-5 h-5" />,
      selected: true,
      color: 'bg-yellow-500'
    },
    {
      id: 'pressure',
      name: 'Pressure',
      value: 1013,
      unit: 'hPa',
      icon: <Gauge className="w-5 h-5" />,
      selected: false,
      color: 'bg-purple-500'
    },
    {
      id: 'uv',
      name: 'UV',
      value: 3,
      unit: '',
      icon: <SunDim className="w-5 h-5" />,
      selected: false,
      color: 'bg-red-500'
    }
  ])

  const [showSettings, setShowSettings] = useState(false)
  const [updateInterval, setUpdateInterval] = useState(1000)
  const [darkMode, setDarkMode] = useState(true) // Default to dark mode for glasses

  // Simulate real-time data updates
  useEffect(() => {
    const interval = setInterval(() => {
      setSensors(prevSensors => prevSensors.map(sensor => ({
        ...sensor,
        value: sensor.selected ? getRandomValue(sensor.id, sensor.value) : sensor.value
      })))
    }, updateInterval)

    return () => clearInterval(interval)
  }, [updateInterval])

  const getRandomValue = (id: string, currentValue: number): number => {
    const fluctuation = Math.random() * 2 - 1
    switch(id) {
      case 'temp': return Math.max(15, Math.min(35, currentValue + fluctuation * 0.2))
      case 'humidity': return Math.max(30, Math.min(80, currentValue + fluctuation * 0.5))
      case 'light': return Math.max(0, Math.min(2000, currentValue + fluctuation * 10))
      case 'pressure': return Math.max(980, Math.min(1040, currentValue + fluctuation * 0.5))
      case 'uv': return Math.max(0, Math.min(11, currentValue + fluctuation * 0.1))
      default: return currentValue
    }
  }

  const toggleSensor = (sensorId: string) => {
    setSensors(prevSensors => 
      prevSensors.map(sensor => 
        sensor.id === sensorId 
          ? { ...sensor, selected: !sensor.selected } 
          : sensor
      )
    )
  }

  const handleUpdateIntervalChange = (value: number[]) => {
    setUpdateInterval(value[0])
  }

  const visibleSensors = sensors.filter(sensor => sensor.selected)

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-950 text-gray-100' : 'bg-gray-50 text-gray-900'} p-4 transition-colors`}>
      <div className="max-w-md mx-auto"> {/* Narrower container for glasses UI */}
        {/* Header with larger text for visibility */}
        <header className="mb-6">
          <h1 className={`text-2xl font-bold mb-1 ${darkMode ? 'text-blue-400' : 'text-blue-600'}`}>SENSOR DASHBOARD</h1>
          <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Real-time monitoring</p>
        </header>

        {/* Settings Button - Larger for touch */}
        <div className="mb-4 flex justify-end">
          <Button 
            variant="outline" 
            onClick={() => setShowSettings(!showSettings)}
            className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-300'}`}
            size="lg"
          >
            <Settings className="mr-2 h-5 w-5" />
            SETTINGS
          </Button>
        </div>

        {/* Settings Panel */}
        {showSettings && (
          <Card className={`mb-6 ${darkMode ? 'bg-gray-900 border-gray-800' : ''}`}>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle className="text-lg">SETTINGS</CardTitle>
              <Button 
                variant="ghost" 
                size="icon" 
                onClick={() => setShowSettings(false)}
                className="rounded-full"
              >
                <X className="h-5 w-5" />
              </Button>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <Label htmlFor="dark-mode" className="text-sm">DARK MODE</Label>
                <Switch 
                  id="dark-mode" 
                  checked={darkMode} 
                  onCheckedChange={setDarkMode}
                  className="data-[state=checked]:bg-blue-500"
                />
              </div>
              
              <div>
                <Label htmlFor="update-interval" className="text-sm">
                  UPDATE: {updateInterval}ms
                </Label>
                <Slider
                  id="update-interval"
                  defaultValue={[updateInterval]}
                  min={200}
                  max={3000}
                  step={100}
                  onValueChange={handleUpdateIntervalChange}
                  className="mt-3"
                />
              </div>

              <div>
                <Label className="text-sm">ACTIVE SENSORS</Label>
                <div className="mt-3 space-y-3">
                  {sensors.map(sensor => (
                    <div key={sensor.id} className="flex items-center justify-between">
                      <Label htmlFor={`sensor-${sensor.id}`} className="flex items-center gap-2">
                        <span className={`w-3 h-3 rounded-full ${sensor.color}`}></span>
                        {sensor.name}
                      </Label>
                      <Switch
                        id={`sensor-${sensor.id}`}
                        checked={sensor.selected}
                        onCheckedChange={() => toggleSensor(sensor.id)}
                        className="data-[state=checked]:bg-blue-500"
                      />
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-end">
              <Button 
                onClick={() => setShowSettings(false)}
                className="bg-blue-600 hover:bg-blue-700"
                size="lg"
              >
                <Check className="mr-2 h-5 w-5" />
                APPLY
              </Button>
            </CardFooter>
          </Card>
        )}

        {/* Sensor Cards - Simplified for small displays */}
        {visibleSensors.length === 0 ? (
          <div className="text-center py-8">
            <p className={darkMode ? 'text-gray-500' : 'text-gray-400'}>
              No active sensors. Enable sensors in settings.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-3">
            {visibleSensors.map(sensor => (
              <Card 
                key={sensor.id} 
                className={`${darkMode ? 'bg-gray-900 border-gray-800' : 'bg-white'} p-3`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className={`text-xs font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                    {sensor.name}
                  </div>
                  <div className={`p-1 rounded-full ${sensor.color} bg-opacity-20`}>
                    {sensor.icon}
                  </div>
                </div>
                <div className="text-2xl font-bold tracking-tight">
                  {sensor.value.toFixed(sensor.unit === '%' ? 0 : 1)}
                  <span className="text-sm ml-0.5">{sensor.unit}</span>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Status Bar */}
        <div className={`mt-6 text-center text-xs ${darkMode ? 'text-gray-600' : 'text-gray-500'}`}>
          <p>v1.0 | {new Date().toLocaleTimeString()}</p>
        </div>
      </div>
    </div>
  )
}