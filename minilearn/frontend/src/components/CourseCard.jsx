function CourseCard({ course, onDetails, onEnroll }) {
  const provider = course.provider || "MiniLearn Academy";
  const rating = course.rating ?? "4.8";
  const enrollmentCount = course.enrollmentCount ?? 1200;

  return (
    <article className="course-card">
      <div className="course-card-topline">
        <span className="course-level">{course.level || "All levels"}</span>
        <span className="course-rating">★ {rating}</span>
      </div>
      <h3>{course.title}</h3>
      <p className="course-provider">{provider}</p>
      <p className="course-description">
        {course.description || "Build practical skills with guided, hands-on learning."}
      </p>
      <div className="course-meta">
        <span><strong>ID</strong> {course.learningId}</span>
        <span><strong>Time</strong> {course.durationHours || 0}h</span>
        <span><strong>Learners</strong> {Number(enrollmentCount).toLocaleString()}</span>
      </div>
      <div className="course-actions">
        <button className="details-button" type="button" onClick={() => onDetails(course)}>
          View details
        </button>
        <button className="enroll-button" type="button" onClick={() => onEnroll(course)}>
          Enroll
        </button>
      </div>
    </article>
  );
}

export default CourseCard;
