import { NavLink } from 'react-router-dom'
import logoIcon from '../assets/logo.svg'

const navItems = [
  { label: 'Features', href: '/#features' },
  { label: 'How It Works', href: '/#how-it-works' },
  { label: 'Voice', href: '/#voice' },
  { label: 'Pricing', href: '/#pricing' },
  { label: 'Blog', href: '/blogs', highlight: false },
]

export default function Navbar() {
  return (
    <header className="absolute top-0 w-full z-50">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-6 lg:px-8">
        <NavLink to="/" className="flex items-center gap-3">
          <img src={logoIcon} alt="" className="h-10 object-contain" />
          <span className="text-xl font-serif tracking-wide">
            <span className="text-gold">WonderTales</span> <span className="text-white">Hub</span>
          </span>
        </NavLink>

        <nav className="hidden items-center gap-10 md:flex ml-10">
          {navItems.map((item) => (
            <a
              key={item.label}
              href={item.href}
              className={`text-[13px] font-normal transition-colors text-white hover:text-gold`}
            >
              {item.label}
            </a>
          ))}
        </nav>

        <a
          href="/#pricing"
          className="rounded-md bg-gradient-to-r from-orange-300 via-orange-400 to-orange-500 px-6 py-2.5 text-[13px] font-semibold text-white transition hover:opacity-90"
        >
          Get Download link
        </a>
      </div>
    </header>
  )
}
