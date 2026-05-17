import footerImg from '../../assets/footerimg.png'
import storeButtons from '../../assets/google and apple playstore.svg'

export default function CTA() {
  return (
    <section className="relative px-6 py-24 lg:px-8 overflow-hidden min-h-[500px] flex items-center justify-center" style={{ backgroundImage: `url('${footerImg}')`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
      <div className="absolute inset-0 bg-navy-950/40 z-0" />
      <div className="absolute inset-x-0 top-0 h-48 bg-gradient-to-b from-navy-950 to-transparent z-0" />
      <div className="relative z-10 mx-auto max-w-3xl text-center">
        <p className="text-sm font-medium text-gold tracking-widest uppercase">Ready to Begin?</p>
        <h2 className="mt-4 font-serif text-4xl text-white sm:text-5xl leading-tight">
          Start Your Child's<br />Magical Journey Tonight
        </h2>
        <div className="mt-10 flex justify-center">
          <img src={storeButtons} alt="Download on App Store and Google Play" className="h-12 object-contain" />
        </div>
      </div>
    </section>
  )
}
