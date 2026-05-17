import howItWorksImage from '../../assets/howitworksimg.png'
import waveImg from '../../assets/wave.svg'
import icon1 from '../../assets/cartoon-boy-with-backpack-tablet 1.png'
import icon2 from '../../assets/image 23.png'
import icon3 from '../../assets/image 20.png'

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="relative overflow-hidden px-6 py-24 lg:px-8 min-h-[600px] flex items-center">
      {/* Wave Background */}
      <div className="absolute inset-0 z-0 opacity-30">
        <img src={waveImg} alt="" className="w-full h-full object-cover" />
      </div>

      {/* Background image anchored to the right, scaling to height */}
      <div className="absolute inset-y-0 right-0 w-[80%] md:w-[60%] lg:w-[50%] max-w-[930px] z-0">
        <img src={howItWorksImage} alt="" className="w-full h-full object-cover object-left" />
        <div className="absolute inset-0 bg-gradient-to-r from-navy-950 via-navy-950/80 to-transparent" />
      </div>
      
      <div className="absolute inset-0 bg-navy-950/20 z-0" />

      <div className="relative z-10 mx-auto w-full max-w-7xl">
        <div className="max-w-2xl space-y-12">
          <div>
            <p className="text-sm font-medium text-gold tracking-widest uppercase">How It Works</p>
            <h2 className="mt-4 font-serif text-4xl text-white sm:text-5xl lg:text-6xl leading-[1.1]">
              Create Magical Stories<br />in <span className="text-gold">3</span> Simple Steps
            </h2>
          </div>

          <div className="grid gap-6 sm:grid-cols-3">
            {[
              { icon: icon1, title: 'Create Your Child', desc: 'Create or select profile to personalize their story.' },
              { icon: icon2, title: 'Create Story', desc: 'Choose a theme, length & Voice to generate a story.' },
              { icon: icon3, title: 'Listen & Enjoy', desc: 'Sit back, relax & enjoy magical story anytime anywhere.' },
            ].map((s) => (
              <div key={s.title} className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-md p-6 text-left shadow-xl">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-navy-800 border border-white/10 mb-4 p-2">
                  <img src={s.icon} alt="" className="w-full h-full object-contain" />
                </div>
                <h3 className="text-sm font-medium text-gold">{s.title}</h3>
                <p className="mt-2 text-xs text-white/60 font-light leading-relaxed">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

