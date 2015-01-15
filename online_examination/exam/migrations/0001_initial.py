# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subject'
        db.create_table(u'exam_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('total_mark', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('pass_mark', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'exam', ['Subject'])

        # Adding model 'Exam'
        db.create_table(u'exam_exam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exam_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Course'], null=True, blank=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Batch'], null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('no_subjects', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('exam_total', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'exam', ['Exam'])

        # Adding M2M table for field subjects on 'Exam'
        db.create_table(u'exam_exam_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('exam', models.ForeignKey(orm[u'exam.exam'], null=False)),
            ('subject', models.ForeignKey(orm[u'exam.subject'], null=False))
        ))
        db.create_unique(u'exam_exam_subjects', ['exam_id', 'subject_id'])

        # Adding model 'SubjectMark'
        db.create_table(u'exam_subjectmark', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exam.Subject'], null=True, blank=True)),
            ('mark', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'exam', ['SubjectMark'])

        # Adding model 'StudentMark'
        db.create_table(u'exam_studentmark', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academic.Student'], null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Course'], null=True, blank=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Batch'], null=True, blank=True)),
            ('exam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exam.Exam'], null=True, blank=True)),
            ('total_mark', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'exam', ['StudentMark'])

        # Adding M2M table for field subject_mark on 'StudentMark'
        db.create_table(u'exam_studentmark_subject_mark', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentmark', models.ForeignKey(orm[u'exam.studentmark'], null=False)),
            ('subjectmark', models.ForeignKey(orm[u'exam.subjectmark'], null=False))
        ))
        db.create_unique(u'exam_studentmark_subject_mark', ['studentmark_id', 'subjectmark_id'])

    def backwards(self, orm):
        # Deleting model 'Subject'
        db.delete_table(u'exam_subject')

        # Deleting model 'Exam'
        db.delete_table(u'exam_exam')

        # Removing M2M table for field subjects on 'Exam'
        db.delete_table('exam_exam_subjects')

        # Deleting model 'SubjectMark'
        db.delete_table(u'exam_subjectmark')

        # Deleting model 'StudentMark'
        db.delete_table(u'exam_studentmark')

        # Removing M2M table for field subject_mark on 'StudentMark'
        db.delete_table('exam_studentmark_subject_mark')

    models = {
        u'academic.student': {
            'Meta': {'object_name': 'Student'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Batch']", 'null': 'True', 'blank': 'True'}),
            'blood_group': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificates_file': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificates_remarks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificates_submitted': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Course']", 'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'doj': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_land_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_proofs_file': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id_proofs_remarks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id_proofs_submitted': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'land_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qualified_exam': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['college.QualifiedExam']", 'null': 'True', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'roll_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'student_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'technical_qualification': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['college.TechnicalQualification']", 'null': 'True', 'blank': 'True'})
        },
        u'college.batch': {
            'Meta': {'object_name': 'Batch'},
            'batch': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.CourseBranch']", 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Course']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'college.course': {
            'Meta': {'object_name': 'Course'},
            'course': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'college.coursebranch': {
            'Meta': {'object_name': 'CourseBranch'},
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'college.qualifiedexam': {
            'Meta': {'object_name': 'QualifiedExam'},
            'authority': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'college.technicalqualification': {
            'Meta': {'object_name': 'TechnicalQualification'},
            'authority': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'exam.exam': {
            'Meta': {'object_name': 'Exam'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Batch']", 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Course']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'exam_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'exam_total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_subjects': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['exam.Subject']", 'null': 'True', 'blank': 'True'})
        },
        u'exam.studentmark': {
            'Meta': {'object_name': 'StudentMark'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Batch']", 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Course']", 'null': 'True', 'blank': 'True'}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exam.Exam']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['academic.Student']", 'null': 'True', 'blank': 'True'}),
            'subject_mark': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['exam.SubjectMark']", 'null': 'True', 'blank': 'True'}),
            'total_mark': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'exam.subject': {
            'Meta': {'object_name': 'Subject'},
            'end_time': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pass_mark': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'subject_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'total_mark': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'exam.subjectmark': {
            'Meta': {'object_name': 'SubjectMark'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'subject_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exam.Subject']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['exam']