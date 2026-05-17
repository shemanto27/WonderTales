import BlogCard from '../components/BlogCard'
import { useBlogStore } from '../cotexts/blogStore'

export default function BlogsPage() {
  const blogs = useBlogStore((state) => state.blogs)

  return (
    <div className="bg-navy-950 px-6 py-16 lg:px-8 min-h-[60vh]">
      <div className="mx-auto max-w-7xl">
        <h1 className="font-serif text-4xl text-white sm:text-5xl">
          <span className="text-gold">Blogs</span> for Children
        </h1>

        <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {blogs.map((post) => (
            <BlogCard key={post.slug} post={post} />
          ))}
        </div>
      </div>
    </div>
  )
}
