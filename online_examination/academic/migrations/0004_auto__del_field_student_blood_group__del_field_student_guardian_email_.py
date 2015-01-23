# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Student.blood_group'
        db.delete_column(u'academic_student', 'blood_group')

        # Deleting field 'Student.guardian_email'
        db.delete_column(u'academic_student', 'guardian_email')

        # Deleting field 'Student.id_proofs_submitted'
        db.delete_column(u'academic_student', 'id_proofs_submitted')

        # Deleting field 'Student.certificates_file'
        db.delete_column(u'academic_student', 'certificates_file')

        # Deleting field 'Student.guardian_address'
        db.delete_column(u'academic_student', 'guardian_address')

        # Deleting field 'Student.land_number'
        db.delete_column(u'academic_student', 'land_number')

        # Deleting field 'Student.relationship'
        db.delete_column(u'academic_student', 'relationship')

        # Deleting field 'Student.id_proofs_remarks'
        db.delete_column(u'academic_student', 'id_proofs_remarks')

        # Deleting field 'Student.certificates_remarks'
        db.delete_column(u'academic_student', 'certificates_remarks')

        # Deleting field 'Student.guardian_land_number'
        db.delete_column(u'academic_student', 'guardian_land_number')

        # Deleting field 'Student.certificates_submitted'
        db.delete_column(u'academic_student', 'certificates_submitted')

        # Deleting field 'Student.doj'
        db.delete_column(u'academic_student', 'doj')

        # Deleting field 'Student.id_proofs_file'
        db.delete_column(u'academic_student', 'id_proofs_file')

        # Deleting field 'Student.batch'
        db.delete_column(u'academic_student', 'batch_id')

        # Deleting field 'Student.guardian_name'
        db.delete_column(u'academic_student', 'guardian_name')

        # Deleting field 'Student.roll_number'
        db.delete_column(u'academic_student', 'roll_number')

        # Adding field 'Student.registration_no'
        db.add_column(u'academic_student', 'registration_no',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.hall_ticket_no'
        db.add_column(u'academic_student', 'hall_ticket_no',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.semester'
        db.add_column(u'academic_student', 'semester',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Semester'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.age'
        db.add_column(u'academic_student', 'age',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.permanent_address'
        db.add_column(u'academic_student', 'permanent_address',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field qualified_exam on 'Student'
        db.delete_table('academic_student_qualified_exam')

        # Removing M2M table for field technical_qualification on 'Student'
        db.delete_table('academic_student_technical_qualification')

    def backwards(self, orm):
        # Adding field 'Student.blood_group'
        db.add_column(u'academic_student', 'blood_group',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.guardian_email'
        db.add_column(u'academic_student', 'guardian_email',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.id_proofs_submitted'
        db.add_column(u'academic_student', 'id_proofs_submitted',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.certificates_file'
        db.add_column(u'academic_student', 'certificates_file',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.guardian_address'
        db.add_column(u'academic_student', 'guardian_address',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.land_number'
        db.add_column(u'academic_student', 'land_number',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.relationship'
        db.add_column(u'academic_student', 'relationship',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.id_proofs_remarks'
        db.add_column(u'academic_student', 'id_proofs_remarks',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.certificates_remarks'
        db.add_column(u'academic_student', 'certificates_remarks',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.guardian_land_number'
        db.add_column(u'academic_student', 'guardian_land_number',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.certificates_submitted'
        db.add_column(u'academic_student', 'certificates_submitted',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.doj'
        db.add_column(u'academic_student', 'doj',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.id_proofs_file'
        db.add_column(u'academic_student', 'id_proofs_file',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.batch'
        db.add_column(u'academic_student', 'batch',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Batch'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.guardian_name'
        db.add_column(u'academic_student', 'guardian_name',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Student.roll_number'
        db.add_column(u'academic_student', 'roll_number',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Student.registration_no'
        db.delete_column(u'academic_student', 'registration_no')

        # Deleting field 'Student.hall_ticket_no'
        db.delete_column(u'academic_student', 'hall_ticket_no')

        # Deleting field 'Student.semester'
        db.delete_column(u'academic_student', 'semester_id')

        # Deleting field 'Student.age'
        db.delete_column(u'academic_student', 'age')

        # Deleting field 'Student.permanent_address'
        db.delete_column(u'academic_student', 'permanent_address')

        # Adding M2M table for field qualified_exam on 'Student'
        db.create_table(u'academic_student_qualified_exam', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm[u'academic.student'], null=False)),
            ('qualifiedexam', models.ForeignKey(orm[u'college.qualifiedexam'], null=False))
        ))
        db.create_unique(u'academic_student_qualified_exam', ['student_id', 'qualifiedexam_id'])

        # Adding M2M table for field technical_qualification on 'Student'
        db.create_table(u'academic_student_technical_qualification', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm[u'academic.student'], null=False)),
            ('technicalqualification', models.ForeignKey(orm[u'college.technicalqualification'], null=False))
        ))
        db.create_unique(u'academic_student_technical_qualification', ['student_id', 'technicalqualification_id'])

    models = {
        u'academic.student': {
            'Meta': {'object_name': 'Student'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Course']", 'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'hall_ticket_no': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'permanent_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'registration_no': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Semester']", 'null': 'True', 'blank': 'True'}),
            'student_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'college.course': {
            'Meta': {'object_name': 'Course'},
            'course': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['college.Semester']", 'null': 'True', 'blank': 'True'})
        },
        u'college.semester': {
            'Meta': {'object_name': 'Semester'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['academic']