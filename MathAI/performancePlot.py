#performancePlot.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.linear_model import LinearRegression


def generate_performance_report(data):
    topics = ["0", "1", "2", "3", "4"]
    rounds = np.array(range(1, len(data) + 1))
    pdf_filename = "performance_report.pdf"

    with PdfPages(pdf_filename) as pdf:
        plt.figure(figsize=(10, 15))  # Adjust size to fit all plots on one page
        for i, topic in enumerate(topics):
            scores = np.array([entry[topic] for entry in data])
            ax = plt.subplot(len(topics), 1, i + 1)
            ax.plot(
                rounds,
                scores,
                marker="o",
                linestyle="-",
                label=f"Scores for Topic {topic}",
            )

            model = LinearRegression().fit(rounds.reshape(-1, 1), scores)
            trend_line = model.predict(rounds.reshape(-1, 1))
            ax.plot(rounds, trend_line, color="red", linestyle="--", label="Trend Line")

            ax.set_title(f"Topic {topic}")
            ax.set_ylabel("Score (%)")
            if i == len(topics) - 1:  # Only label x-axis for the last plot
                ax.set_xlabel("Round")
            ax.legend()
            ax.grid(True)

            # Perform analysis and annotate directly on the subplot
            slope = model.coef_[0]
            recent_performance = scores[-1]
            trend_analysis = (
                "Improving" if slope > 0 else "Declining" if slope < 0 else "Stable"
            )
            performance_analysis = (
                "Excellent performance"
                if recent_performance >= 80
                else (
                    "Good performance"
                    if recent_performance >= 60
                    else "Needs improvement"
                )
            )
            analysis_text = f"Trend: {trend_analysis}, {performance_analysis}"
            ax.annotate(
                analysis_text,
                xy=(0.5, -0.15),
                xycoords="axes fraction",
                ha="center",
                va="top",
                fontsize=10,
            )

        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f"PDF report generated: {pdf_filename}")
