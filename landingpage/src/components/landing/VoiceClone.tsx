import waveImg from '../../assets/wave.svg'
import micImg from '../../assets/mic.svg'
import avatar1 from '../../assets/image 23.png'
import mobileAppImage from '../../assets/mobileapp.svg'
 
export default function VoiceClone() {
  return (
    <section id="voice" className="relative px-6 py-12 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <div className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-transparent p-6 sm:p-10 shadow-2xl shadow-black/40">
          
          <div className="absolute inset-0 opacity-25 z-0 pointer-events-none">
             <img src={waveImg} alt="" className="w-full h-full object-cover" />
          </div>
 
          <div className="relative z-10 flex flex-col gap-8 lg:flex-row lg:items-center justify-between w-full">
            <div className="max-w-md space-y-3 text-left">
              <p className="text-xs font-semibold text-gold tracking-widest uppercase">Your Voice, Their Comfort</p>
              <h2 className="font-serif text-3xl sm:text-4xl text-white leading-tight">Clone Your Voice<br />in Seconds</h2>
              <p className="text-xs sm:text-sm text-white/70 font-light leading-relaxed">
                Record your voice and let our AI create a perfect clone to narrate stories for your child.
              </p>
            </div>
            
            <div className="flex items-center gap-6 md:gap-8">
              {/* Glowing Glass Mic Circle */}
              <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full border border-white/20 bg-white/5 backdrop-blur-md shadow-lg shadow-gold/5 hover:scale-105 transition-transform duration-300">
                <img src={micImg} alt="Mic" className="h-5 w-5 filter brightness-125" />
              </div>
              
              {/* Voice Clone Dad/Mom Badge */}
              <div className="flex items-center gap-3 rounded-2xl bg-white/5 border border-white/10 px-4 py-3 backdrop-blur-md">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full overflow-hidden border border-white/10">
                  <img src={avatar1} alt="" className="w-full h-full object-cover" />
                </div>
                <div className="text-left">
                  <p className="text-[10px] font-light text-white/60 uppercase tracking-wider">Voice Clone</p>
                  <p className="text-xs font-medium text-white">Ready Mom's Voice</p>
                </div>
              </div>
 
              {/* Compact Phone Mockup */}
              <div className="hidden sm:block h-48 w-24 shrink-0 hover:scale-105 transition-transform duration-500">
                <img src={mobileAppImage} alt="Mobile App" className="h-full w-full object-contain" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
