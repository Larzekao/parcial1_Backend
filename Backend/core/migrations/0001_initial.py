# Generated manually to align with core models
from django.db import migrations, models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
import django.db.models.deletion
from django.core.validators import MinValueValidator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telefono', models.CharField(blank=True, max_length=30)),
                ('estado', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('rol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuarios', to='core.rol')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AreaComun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=150)),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])),
                ('descripcion', models.TextField(blank=True)),
                ('estado', models.CharField(default='disponible', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ConceptoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=150)),
                ('tipo', models.PositiveSmallIntegerField(choices=[(1, 'Cuota de mantenimiento'), (2, 'Multa'), (3, 'Reserva de area comun'), (4, 'Otro')])),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=150)),
                ('cargo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('telefono', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Residencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.TextField(blank=True)),
                ('direccion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Residente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=150)),
                ('sexo', models.CharField(blank=True, max_length=10)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('propietario', 'Propietario'), ('inquilino', 'Inquilino'), ('otro', 'Otro')], max_length=20)),
                ('residencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='residentes', to='core.residencia')),
                ('usuario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='residente', to='core.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_programada', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_progreso', 'En progreso'), ('completada', 'Completada'), ('cancelada', 'Cancelada')], default='pendiente', max_length=20)),
                ('personal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tareas', to='core.personal')),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('placa', models.CharField(max_length=20, unique=True)),
                ('modelo', models.CharField(max_length=100)),
                ('color', models.CharField(blank=True, max_length=50)),
                ('residente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehiculos', to='core.residente')),
            ],
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('residencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mascotas', to='core.residencia')),
            ],
        ),
        migrations.CreateModel(
            name='Visitante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=150)),
                ('motivo', models.CharField(blank=True, max_length=255)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to='visitantes/')),
                ('residente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visitantes', to='core.residente')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')], default='pendiente', max_length=20)),
                ('referencia_pago', models.CharField(blank=True, max_length=150)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='core.areacomun')),
                ('residente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='core.residente')),
            ],
            options={
                'ordering': ['-fecha', '-hora_inicio'],
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dia', models.CharField(max_length=50)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='core.areacomun')),
            ],
        ),
        migrations.CreateModel(
            name='Regla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=150)),
                ('descripcion', models.TextField()),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reglas', to='core.areacomun')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateField()),
                ('monto_total', models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('pagada', 'Pagada'), ('vencida', 'Vencida'), ('anulada', 'Anulada')], default='pendiente', max_length=20)),
                ('notas', models.TextField(blank=True)),
                ('residente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facturas', to='core.residente')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=12)),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalles', to='core.conceptopago')),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='core.factura')),
            ],
        ),
        migrations.AddConstraint(
            model_name='horario',
            constraint=models.UniqueConstraint(fields=('area', 'dia', 'hora_inicio', 'hora_fin'), name='core_horario_unique_por_area'),
        ),
        migrations.AddConstraint(
            model_name='reserva',
            constraint=models.UniqueConstraint(fields=('area', 'fecha', 'hora_inicio', 'hora_fin'), name='core_reserva_bloque_unico'),
        ),
    ]