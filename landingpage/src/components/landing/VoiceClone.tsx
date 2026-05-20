import waveImg from '../../assets/wave.svg'
import micImg from '../../assets/mic.svg'
import handImg from '../../assets/handimg.svg'

export default function VoiceClone() {
  return (
    <section id="voice" className="relative px-6 py-12 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <div className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-transparent p-6 sm:p-10 shadow-2xl shadow-black/40">
          
          <div className="absolute inset-0 opacity-25 z-0 pointer-events-none">
             <img src={waveImg} alt="" className="w-full h-full object-cover" />
          </div>
 
          <div className="relative z-10 flex flex-col gap-8 lg:flex-row lg:items-center justify-between w-full h-full min-h-[300px]">
            <div className="max-w-md space-y-3 text-left z-20">
              <p className="text-xs font-semibold text-gold tracking-widest uppercase">Your Voice, Their Comfort</p>
              <h2 className="font-serif text-3xl sm:text-4xl text-white leading-tight">Clone Your Voice<br />in Seconds</h2>
              <p className="text-xs sm:text-sm text-white/70 font-light leading-relaxed">
                Record your voice and let our AI create a perfect clone to narrate stories for your child.
              </p>
            </div>
            
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-10">
              {/* Glowing Glass Mic Circle */}
              <div className="flex h-16 w-16 items-center justify-center rounded-full border border-white/20 bg-white/5 backdrop-blur-md shadow-[0_0_30px_rgba(255,215,0,0.15)] hover:scale-105 transition-transform duration-300">
                <img src={micImg} alt="Mic" className="h-6 w-6 filter brightness-125" />
              </div>
            </div>
            
            <div className="relative z-20 h-full">
              {/* Hand with Phone Mockup */}
              <div className="hidden sm:block absolute right-[-40px] top-[-80px] h-[450px] w-auto shrink-0 hover:scale-105 transition-transform duration-500">
                <img src={handImg} alt="Mobile App in Hand" className="h-full w-full object-contain" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
