import waveImg from '../../assets/wave.svg'
import micImg from '../../assets/mic.svg'
import avatar1 from '../../assets/image 20.png'
import mobileAppImage from '../../assets/mobileapp.svg'

export default function VoiceClone() {
  return (
    <section id="voice" className="px-6 py-12 lg:px-8 relative z-10">
      <div className="mx-auto max-w-7xl">
        <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-navy-900/50 p-8 sm:p-12 backdrop-blur-md">
          
          <div className="absolute inset-0 opacity-20 z-0">
             <img src={waveImg} alt="" className="w-full h-full object-cover" />
          </div>

          <div className="relative z-10 flex flex-col gap-10 lg:flex-row lg:items-center justify-between">
            <div className="max-w-md space-y-4">
              <p className="text-sm font-medium text-gold tracking-widest uppercase">Your Voice, Their Comfort</p>
              <h2 className="font-serif text-4xl text-white sm:text-5xl leading-tight">Clone Your Voice<br />in Seconds</h2>
              <p className="text-sm text-white/70 font-light leading-relaxed">
                Record your voice and let our AI create a perfect clone to narrate stories for your child.
              </p>
            </div>
            
            <div className="flex items-center gap-8">
              <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full border border-gold bg-transparent">
                <img src={micImg} alt="Mic" className="h-6 w-6" />
              </div>
              
              <div className="flex items-center gap-4 rounded-2xl bg-white/5 border border-white/10 px-5 py-4 backdrop-blur-md">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-white/10 overflow-hidden">
                  <img src={avatar1} alt="" className="w-full h-full object-cover" />
                </div>
                <div className="text-center px-2">
                  <p className="text-xs font-light text-white/80">Voice Clone</p>
                  <p className="text-sm font-medium text-white">Ready Dad's Voice</p>
                </div>
              </div>

              <div className="hidden sm:block h-64 w-32 shrink-0">
                <img src={mobileAppImage} alt="Mobile App" className="h-full w-full object-contain" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
