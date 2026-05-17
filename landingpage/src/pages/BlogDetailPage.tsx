import { useParams } from 'react-router-dom'
import { useBlogStore } from '../cotexts/blogStore'

export default function BlogDetailPage() {
  const { slug } = useParams()
  const blog = useBlogStore((state) => state.getBlogBySlug(slug ?? ''))

  if (!blog) {
    return (
      <div className="min-h-[60vh] bg-navy-950 px-6 py-20 text-center text-slate-300 lg:px-8">
        <h2 className="font-serif text-3xl text-white">Blog not found</h2>
        <p className="mt-4 text-sm text-slate-400">The story you're looking for is not available yet.</p>
      </div>
    )
  }

  // Split content into sections based on numbered headings & "The Ultimate Benefit"
  const renderContent = (content: string) => {
    const blocks = content.split('\n\n')
    return blocks.map((block, i) => {
      // Check if block starts with a number like "1. Set the Stage"
      const headingMatch = block.match(/^(\d+\.\s+.+)$/)
      if (headingMatch) {
        return (
          <h2 key={i} className="mt-10 font-serif text-2xl text-gold sm:text-3xl">
            {headingMatch[1]}
          </h2>
        )
      }
      // Check for "The Ultimate Benefit" type headings
      if (block.startsWith('The Ultimate')) {
        return (
          <h2 key={i} className="mt-10 font-serif text-2xl text-gold sm:text-3xl">
            {block}
          </h2>
        )
      }
      // Check for bullet points (lines starting with "•" or "- ")
      if (block.includes('\n•') || block.includes('\n- ')) {
        const lines = block.split('\n')
        return (
          <ul key={i} className="mt-4 space-y-3">
            {lines.map((line, j) => {
              const bulletText = line.replace(/^[•\-]\s*/, '')
              // Check for bold prefix like "Dim the Lights:"
              const boldMatch = bulletText.match(/^(.+?:)\s*(.+)$/)
              if (boldMatch) {
                return (
                  <li key={j} className="text-sm text-slate-300 leading-7 flex gap-2">
                    <span className="text-white mt-1">•</span>
                    <span><strong className="text-white">{boldMatch[1]}</strong> {boldMatch[2]}</span>
                  </li>
                )
              }
              return (
                <li key={j} className="text-sm text-slate-300 leading-7 flex gap-2">
                  <span className="text-white mt-1">•</span>
                  <span>{bulletText}</span>
                </li>
              )
            })}
          </ul>
        )
      }
      return (
        <p key={i} className="mt-4 text-sm text-slate-300 leading-8">
          {block}
        </p>
      )
    })
  }

  return (
    <div className="bg-navy-950 px-6 py-16 lg:px-8">
      <div className="mx-auto max-w-3xl">
        <h1 className="font-serif text-3xl text-gold sm:text-4xl leading-snug">
          {blog.title}
        </h1>

        <img
          src={blog.image}
          alt={blog.title}
          className="mt-8 w-full max-w-md rounded-2xl"
        />

        <div className="mt-10">
          {renderContent(blog.content)}
        </div>
      </div>
    </div>
  )
}
