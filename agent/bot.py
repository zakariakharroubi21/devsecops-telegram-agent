from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gitlab_client import GitLabClient
from config import TELEGRAM_BOT_TOKEN

gitlab = GitLabClient()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
🤖 Agent AI DevSecOps activé.

Commandes disponibles :

/run_pipeline - Lancer le pipeline complet
/scan - Lancer les scans sécurité
/deploy - Lancer le déploiement
/status - Voir l'état du dernier pipeline
/stop_pipeline - Arrêter le dernier pipeline
/logs <job_id> - Afficher les logs d'un job
/help - Afficher l'aide
"""
    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def run_pipeline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.trigger_pipeline(mode="full")

        message = f"""
🚀 Pipeline lancé avec succès.

ID: {pipeline.get("id")}
Status: {pipeline.get("status")}
Ref: {pipeline.get("ref")}
Web URL: {pipeline.get("web_url")}
"""
        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"❌ Erreur lancement pipeline:\n{str(e)}")


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.trigger_pipeline(mode="scan")

        message = f"""
🛡️ Scan sécurité lancé.

Pipeline ID: {pipeline.get("id")}
Status: {pipeline.get("status")}
Web URL: {pipeline.get("web_url")}
"""
        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"❌ Erreur scan:\n{str(e)}")


async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.trigger_pipeline(mode="deploy")

        message = f"""
📦 Déploiement lancé.

Pipeline ID: {pipeline.get("id")}
Status: {pipeline.get("status")}
Web URL: {pipeline.get("web_url")}
"""
        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"❌ Erreur déploiement:\n{str(e)}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.get_latest_pipeline()

        if not pipeline:
            await update.message.reply_text("Aucun pipeline trouvé.")
            return

        pipeline_id = pipeline.get("id")
        jobs = gitlab.get_pipeline_jobs(pipeline_id)

        jobs_text = ""

        for job in jobs:
            jobs_text += f"\n- {job.get('name')} | {job.get('status')} | ID: {job.get('id')}"

        message = f"""
📊 Dernier pipeline :

ID: {pipeline_id}
Status: {pipeline.get("status")}
Ref: {pipeline.get("ref")}
Web URL: {pipeline.get("web_url")}

Jobs:
{jobs_text}
"""
        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"❌ Erreur status:\n{str(e)}")


async def stop_pipeline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.get_latest_pipeline()

        if not pipeline:
            await update.message.reply_text("Aucun pipeline à arrêter.")
            return

        pipeline_id = pipeline.get("id")
        cancelled = gitlab.cancel_pipeline(pipeline_id)

        message = f"""
🛑 Pipeline arrêté.

ID: {cancelled.get("id")}
Status: {cancelled.get("status")}
"""
        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"❌ Erreur arrêt pipeline:\n{str(e)}")


async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("Utilisation: /logs <job_id>")
            return

        job_id = context.args[0]
        logs_text = gitlab.get_job_logs(job_id)

        if len(logs_text) > 3500:
            logs_text = logs_text[-3500:]

        await update.message.reply_text(f"📜 Logs du job {job_id}:\n\n{logs_text}")

    except Exception as e:
        await update.message.reply_text(f"❌ Erreur logs:\n{str(e)}")


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("run_pipeline", run_pipeline))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(CommandHandler("deploy", deploy))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("stop_pipeline", stop_pipeline))
    app.add_handler(CommandHandler("logs", logs))

    print("Agent Telegram DevSecOps running...")
    app.run_polling()


if __name__ == "__main__":
    main()