import { useState, useEffect } from 'react'
import { CloudSun, Sun, CloudRain, Cloud, Snowflake, LocateFixed, RefreshCw } from 'lucide-react'
import { Card, CardContent } from "/components/ui/card"

type WeatherData = {
  temperature: number
  condition: string
  location: string
  humidity: number
  windSpeed: number
  feelsLike: number
  icon: string
}

export default function SmartGlassesWeather() {
  const [weather, setWeather] = useState<WeatherData | null>(null)
  const [isVisible, setIsVisible] = useState(true)
  const [position, setPosition] = useState('top-right')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Simuliramo dobijanje lokacije i vremenskih podataka
  useEffect(() => {
    const fetchLocationAndWeather = async () => {
      try {
        setLoading(true)
        setError(null)
        
        // Simulacija dobijanja lokacije
        const position = await new Promise<GeolocationPosition>((resolve) => {
          navigator.geolocation.getCurrentPosition(resolve, () => {
            // Fallback ako korisnik odbije lokaciju
            resolve({
              coords: {
                latitude: 44.7866, // Beograd
                longitude: 20.4489,
                accuracy: 1,
                altitude: null,
                altitudeAccuracy: null,
                heading: null,
                speed: null
              },
              timestamp: Date.now()
            } as GeolocationPosition)
          })
        })

        // Simulacija API poziva za vreme
        const mockWeatherData = {
          temperature: Math.round(15 + Math.random() * 15),
          condition: ['Sunčano', 'Oblačno', 'Kiša', 'Sneg'][Math.floor(Math.random() * 4)],
          location: await getCityName(position.coords.latitude, position.coords.longitude),
          humidity: Math.round(40 + Math.random() * 50),
          windSpeed: Math.round(1 + Math.random() * 15),
          feelsLike: Math.round(15 + Math.random() * 15),
          icon: ['01d', '02d', '03d', '09d', '13d'][Math.floor(Math.random() * 5)]
        }

        setWeather(mockWeatherData)
      } catch (err) {
        setError('Nismo uspeli da dobijemo vremenske podatke')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchLocationAndWeather()
    
    // Osvežavamo podatke svakih 5 minuta
    const interval = setInterval(fetchLocationAndWeather, 300000)
    return () => clearInterval(interval)
  }, [])

  // Simulacija dobijanja imena grada
  const getCityName = async (lat: number, lon: number): Promise<string> => {
    const cities = [
      { lat: 44.7866, lon: 20.4489, name: 'Beograd, RS' },
      { lat: 45.2534, lon: 19.8319, name: 'Novi Sad, RS' },
      { lat: 43.8563, lon: 18.4131, name: 'Sarajevo, BIH' },
      { lat: 42.4602, lon: 19.2595, name: 'Podgorica, MNE' },
      { lat: 41.9973, lon: 21.4280, name: 'Skoplje, MK' }
    ]
    
    const foundCity = cities.find(city => 
      Math.abs(city.lat - lat) < 1 && Math.abs(city.lon - lon) < 1
    )
    
    return foundCity?.name || 'Nepoznata lokacija'
  }

  const getWeatherIcon = (iconCode?: string) => {
    if (!iconCode) return <CloudSun className="w-8 h-8 text-amber-400" />
    
    if (iconCode.includes('01')) return <Sun className="w-8 h-8 text-amber-400" />
    if (iconCode.includes('09') || iconCode.includes('10')) return <CloudRain className="w-8 h-8 text-blue-300" />
    if (iconCode.includes('13')) return <Snowflake className="w-8 h-8 text-blue-100" />
    if (iconCode.includes('02') || iconCode.includes('03') || iconCode.includes('04')) return <Cloud className="w-8 h-8 text-gray-300" />
    return <CloudSun className="w-8 h-8 text-amber-300" />
  }

  const toggleVisibility = () => setIsVisible(!isVisible)

  const refreshData = async () => {
    setLoading(true)
    await new Promise(resolve => setTimeout(resolve, 1000))
    setWeather(prev => prev ? {
      ...prev,
      temperature: Math.round(15 + Math.random() * 15),
      windSpeed: Math.round(1 + Math.random() * 15)
    } : null)
    setLoading(false)
  }

  const positionClasses = {
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4'
  }

  if (!isVisible) return null

  return (
    <div className={`fixed ${positionClasses[position]} z-50`}>
      <Card className="bg-opacity-90 bg-slate-800 text-white border border-slate-600 shadow-xl shadow-slate-900/30 min-w-[220px] backdrop-blur-sm">
        <CardContent className="p-3">
          {loading && !weather ? (
            <div className="flex justify-center py-4">
              <RefreshCw className="w-6 h-6 animate-spin text-slate-400" />
            </div>
          ) : error ? (
            <div className="text-red-300 text-sm">{error}</div>
          ) : weather ? (
            <>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="text-4xl font-light text-slate-100">
                    {weather.temperature}°C
                  </div>
                  <div>
                    {getWeatherIcon(weather.icon)}
                  </div>
                </div>
                <button 
                  onClick={refreshData}
                  disabled={loading}
                  className="text-slate-300 hover:text-blue-400 disabled:opacity-30 transition-colors"
                >
                  <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                </button>
              </div>
              
              <div className="mt-1">
                <div className="flex items-center text-sm text-slate-300">
                  <LocateFixed className="w-3 h-3 mr-1 text-blue-400" />
                  <span>{weather.location}</span>
                </div>
                <div className="text-xs text-slate-400 mt-1">{weather.condition}</div>
              </div>
              
              <div className="mt-2 pt-2 border-t border-slate-700 text-xs flex justify-between">
                <span className="text-slate-400">Osećaj: <span className="text-slate-200">{weather.feelsLike}°C</span></span>
              </div>
              
              <div className="mt-1 text-xs flex justify-between text-slate-400">
                <span>Vlažnost: <span className="text-slate-200">{weather.humidity}%</span></span>
                <span>Vetar: <span className="text-slate-200">{weather.windSpeed} km/h</span></span>
              </div>
              
              <div className="mt-3 flex justify-between text-xs">
                <button 
                  onClick={toggleVisibility}
                  className="text-slate-400 hover:text-slate-200 transition-colors"
                >
                  Sakrij
                </button>
                <button 
                  onClick={() => setPosition(
                    position === 'top-right' ? 'top-left' : 
                    position === 'top-left' ? 'bottom-left' :
                    position === 'bottom-left' ? 'bottom-right' : 'top-right'
                  )}
                  className="text-slate-400 hover:text-slate-200 transition-colors"
                >
                  Pomeri
                </button>
              </div>
            </>
          ) : null}
        </CardContent>
      </Card>
    </div>
  )
}